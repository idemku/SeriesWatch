SeriesWatch
===========
Projekt eszközök beadandó

**Figyelem!**

A program futtatásához szükség van egy
[**THEMOVIEDB**-s API kulcsra.](https://www.themoviedb.org/faq/api)
A kulcsot ingyen lehet igényelni a hivatalos weboldalukon, ez
viszont regisztráció köteles, ahol meg kell adni néhány személyes
információt.

Ezen kulcs hiányában nem fog működni a program, épp ezért
a [series.demq.hu](https://series.demq.hu) weboldalon elérhető az
applikáció tesztelésre.

Tartalomjegyzék
===============
* [Előzetes követelmények](#előzetes-követelmények)
* [Telepítés](#telepítés)
* [Email értesítő](#email-értesítő)
* [Tesztelés](#tesztelés)

Előzetes követelmények
======================
* Python3
* Django keretrendszer
* TheMovieDb API kulcs

Telepítés
=========
Telepítsd fel a Python 3-at: https://www.python.org/downloads/

Nyiss egy parancssort/terminált és ellenőrizd a verziót:
```
python --version
```
Ez után telepítsd a Django-t és ellenőrizd a verziót (ez utóbbi opcionális): 
```
pip install django
python -m django --version
```

Ha eddig nem tetted, töltsd le a projektet a Githubról.

Hozz létre a projekt főkönyvtárába egy **conf.cnf** fájlt a
**conf_example.cnf** mintájára és ebben add meg a
[themoviedb](https://www.themoviedb.org)-ről igényelt API kulcsot.

**conf.cnf** magyarázat:

*[SW]*
* apiKey - [themoviedb](https://www.themoviedb.org)-ről igényelt API kulcs
* language - Lekérdezések eredményeinek nyelve

*[SMTP]*
* server - kimenő e-mail szerver címe (ami SMTP protokollt használ)
* port - kimenő e-mail szerver portja
* email - kimenő e-mail cím
* user - kimenő e-mail címhez tartozó felhasználónév (megegyezhet az email címmel)
* passw - kimenő e-mailhez tartozó jelszó

Hozd létre az adatbázist és a szükséges adattáblákat a következő
parancsokkal a projekt főkönyvtárában állva:
```
python manage.py makemigrations series
python manage.py makemigrations
python manage.py migrate
```
Így tudsz létrehozni admin fiókot:
```
python manage.py createsuperuser
```
_(Felhasználói teszt fiók létrehozása lejebb)_

A projekt főkönyvtárában a következő paranccsal tudod elindítani a szervert:
```
python manage.py runserver
```
Valami ehhez hasonlót fogsz látni, ha mindent jól csináltál:
```
Performing system checks...

System check identified no issues (0 silenced).

You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.

March 22, 2018 - 15:50:53
Django version 2.0, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

A böngésződből itt fogod elérni: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


Ez után a [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
felületen a létrehozott fiókkal bejelentkezve a **Users** táblában
tudsz létrehozni teszt fiókokat.


Email értesítő
==============
Használat:
- A conf-example.cnf mintájára ki kell tölteni az általad létrehozott conf.cnf
 fáljt a megfelelő adatokkal.
- Az értesítések kiküldéséhez a parancs:
```
python manage.py sendemails
```
Értesítés csak akkor kerül kiküldésre, ha van olyan sorozatra feliratkozás,
ami a parancs futtatásának napján jelenik meg.
Csak azon sorozatok címei lesznek a levélben, amik épp megjelennek.

Az automatizáláshoz crontab-ra állítsd be a fenti parancsot, Windows-os környezetben
egyéb hasonló programban állítsd be a futtatást.

A [series.demq.hu](https://series.demq.hu) oldal magyar idő szerint
minden reggel 6-kor küld értesítő e-maileket.

Tesztelés
=========
A projekt főkönyvtárában(.../SeriesWatch) kiadandó parancs:
```
python manage.py test
```
Ezután egy hasonló üzenetet kéne látnunk a konzolon:
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..................................................
----------------------------------------------------------------------
Ran 50 tests in 9.142s

OK
Destroying test database for alias 'default'...

```