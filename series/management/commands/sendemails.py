'''
Ez a fájl szolgál az e-mailek kiküldésére.
CRONTAB-on, vagy hasonló szolgáltatásban be kell állítani, hogy a nap melyik pontjában
küldje el az értesítéseket e-mailben.
FONTOS: naponta maximum egyszer legyen levélküldés, mivel ez erőforrásigényes folyamat
és amúgy sem akarjuk fölöslegesen spammelni a felhasználókat

Futtatás: python manage.py sendemails
'''

import smtplib, os, configparser, re, datetime
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.utils import COMMASPACE, formatdate, formataddr
from django.core.management.base import BaseCommand
from series.models import User
from series.views import search_tv_by_id
from SeriesWatch.settings import BASE_DIR


class Command(BaseCommand):
    help = "Kiküldi az értesítő e-maileket a felhasználóknak"

    # E-mail küldés segédfüggvény
    def send_mail(self, send_from, send_from_name, send_to, subject, text,
                  user, passw, files=None, server='127.0.0.1', port='25'):
        assert isinstance(send_to, list)

        # E-mail felépítés, adatok beállítása paraméterek alapján
        msg = MIMEMultipart()
        msg['To'] = COMMASPACE.join(send_to)
        msg['Date'] = formatdate(localtime=True)
        msg['From'] = formataddr((str(Header(send_from_name, 'utf-8')), send_from))
        msg['Subject'] = "%s" % Header(subject, 'utf-8')

        # HTML üzenet csatolása
        msg.attach(MIMEText(text, 'html', 'utf-8'))

        # Esetleges csatolmányok hozzáfűzése
        for f in files or []:
            with open(f, 'rb') as fil:
                msg.attach(MIMEApplication(
                    fil.read(),
                    Content_Disposition='attachment; filename="%s"' % basename(f),
                    Name=basename(f)
                ))

        # Kapcsolódás a szerverhez és üzenet küldés
        try:
            smtp = smtplib.SMTP_SSL(server, port)
            smtp.login(user=user, password=passw)
            smtp.sendmail(send_from, send_to, msg.as_string())
            smtp.close()
        except smtplib.SMTPConnectError:
            self.stdout.write("Nem sikerült kapcsolódni a szerverhez: " + server + ":" + port)
        except smtplib.socket.timeout:
            self.stdout.write("A szerver nem válaszol: timeout")
        except Exception as e:
            self.stdout.write(e)

    def handle(self, *args, **options):

        # Config beolvasása
        self.stdout.write(BASE_DIR)
        config = configparser.ConfigParser()
        config.read((os.path.join(BASE_DIR, 'conf.cnf')))
        if config.sections() == []:
            print("Nem sikerült beolvasni a conf.cnf fájlt. A program leáll...")
            exit(1)

        # E-mail szerver beállítások
        server = config["SMTP"]["server"]
        port = config["SMTP"]["port"]
        from_email = config["SMTP"]["email"]
        email_user = config["SMTP"]["user"]
        passw = config["SMTP"]["passw"]

        # Mai dátum
        today = datetime.datetime.now().strftime('%Y-%m-%d')

        # Sablon üzenet beolvasás
        textfile = open((os.path.join(BASE_DIR, "message.html")), 'rb')
        msg = (textfile.read()).decode("utf-8")

        # Az összes usert az all_users-en keresztül érjük el
        all_users = User.objects.all()
        self.stdout.write("Inicializálás kész.")

        for user in all_users:
            # Csak akkor küldjünk e-mailt, ha kérte a felhasználó
            if user.emailNotify:
                self.stdout.write(user.username + " adatainak összegyűjtése...")
                all_series = user.seriestable_set.all()
                series_to_send = []

                # Lekérdezzük a feliratkozott sorozatainak dátumait
                for serie in all_series:
                    serie_data = search_tv_by_id(serie)
                    if serie_data["next_episode_date"] == today:
                        series_to_send.append(serie_data["name"])

                # Ha van olyan sorozat ami megjelenik, küldjük az üzenetet
                if len(series_to_send) > 0:
                    # A sablonba beillesztjük a felhasználónevet
                    msg = re.sub(r'\{\{ user \}\}', user.username, msg)

                    # A sablonba beillesztjük a sorozatok címeit
                    series_txt = "<ul>"
                    for serie in series_to_send:
                        series_txt += "<li>" + serie + "</li>"
                    series_txt += "</ul>"
                    msg = re.sub(r'\{\{ series \}\}', series_txt, msg)

                    # Üzenet küldés
                    self.stdout.write("Üzenet küldés neki: " + user.username)
                    self.send_mail(from_email, "Series Support", [user.email], "Megjelenő sorozatok értesítő",
                                   msg, email_user, passw, server=server, port=port)

        self.stdout.write("E-mailek kiküldése kész.")
