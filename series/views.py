##
# @file
# File documentation
#

import http.client, urllib.parse, json, configparser, datetime, os
from multiprocessing.pool import ThreadPool
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import SeriesTable, User

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read((os.path.join(BASE_DIR,  'conf.cnf'),))
if config.sections() == []:
    print("Nem sikerült beolvasni a conf.cnf fájlt. A program leáll...")
    exit(1)

api_key = config["SW"]["apiKey"]
language = config["SW"]["language"]

def index(request):
    """Függvény amely a főoldal betöltődésekor fut le. Ez függvény POST metódussal kéri le a sorozatok/filmek adatait.
     GET hívásnál hibát jelez."""
    if request.user.is_authenticated:
        user = request.user.username
    else:
        user = "-1"

    context = {"id": "", "name": "", "vote_average": "", "first_air_date": "",
               "next_episode_date": "", "overview": ""}

    if request.method == "POST":
        try:
            title = request.POST["title"]
            if title != "":
                context = search_tv(title)
        except IndexError:
            try:
                context = search_movie(title)
            except IndexError:
                context["name"] = "Nincs ilyen film/sorozat"
    context["user"] = str(user)
    return render(request, "series/index.html", context)


def login_view(request):
    """Ez a függvény a bejelentkezésért felel. A POST kérésben van a felhásználónév és a jelszó."""
    try:
        user = request.POST["usrname"]
        passw = request.POST["pwd"]
        authenticated = authenticate(request, username=user, password=passw)

        if authenticated is not None:
            login(request, authenticated)
            return redirect("index")
        else:
            context = {"loginerror": "Nem megfelelő felhasználónév/jelszó"}
            return render(request, "series/index.html", context)
    except KeyError:
        return redirect("index")


def logout_view(request):
    """Ez a függvény a kijelentkezést hajtja végre."""
    logout(request)
    return redirect("index")


def register_view(request):
    """Ez a függvény a regisztrációért felel. Ellenőrizzük, hogy a megadott 2 jelszó egyezik-e, illetve,
    hogy létezik-e már ilyen felhasználó.
    Felhasználónevet, e-mail címet és a jelszót kell megadni a regisztráláshoz."""
    try:
        user = request.POST["usrname-r"]
        email = request.POST["email-r"]
        pass1 = request.POST["pwd-r"]
        pass2 = request.POST["pwd-r2"]
        emailnotify = False
        if "emailNotify" in request.POST:
            emailnotify = True

        if pass1 != pass2:
            context = {"regerror": "A megadott jelszavak nem egyeznek meg."}
            return render(request, "series/index.html", context)
        else:
            try:
                # Ha ez lefut, akkor már van ilyen user a db-ben
                dbuser = User.objects.get(username=user)
                context = {"regerror": "Már van ilyen nevű felhasználó: " + dbuser.username}
                return render(request, "series/index.html", context)
            except ObjectDoesNotExist:
                User.objects.create_user(username=user, email=email, password=pass1, emailNotify=emailnotify)
            return redirect("index")
    except KeyError:
        return redirect("index")


@login_required
def subscribe(request, series_id):
    """Itt tudunk feliratkozni sorozatokra. Ellenőrzi, hogy létezik-e a megadott azonosítóval sorozat,
     hibás azonosító esetén visszairányít a főoldalra, ha minden rendben lefut
    akkor is a főoldalra irányít. A feliratkozás használatához bejelentkezés szükséges."""
    # Ellenőrizzük, hogy létezik-e ilyen azonosítóval sorozat
    # létrehozza a kapcsolatot
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"

    # összefűzzük a linket a lekérdezéshez
    link = "/3/tv/"
    link += urllib.parse.quote(str(series_id)) + "?"
    link += urllib.parse.urlencode({"language": language, "api_key": api_key})

    conn.request("GET", link, payload)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))

    if "status_code" in json_data:
        # Hibás azonosító, visszaírányít a kezdőoldalra
        return render(request, "series/index.html", {})

    try:
        # Megpróbálja létrehozni az adott azonosító
        serie = SeriesTable.objects.create(seriesID=series_id)
    except IntegrityError:
        # Ha már létezik, akkor csak lekéri a DB-ből
        serie = SeriesTable.objects.get(seriesID=series_id)
    user = User.objects.get(username=request.user.username)
    serie.users.add(user)
    return redirect("index")  # Ha kész, visszadob a kezdőoldalra

@login_required
def unsubscribe(request, series_id):
    """Sorozatról tudunk leiratkozni. Használatához bejelentkezés szükséges."""
    user = User.objects.get(username=request.user.username)
    serie = SeriesTable.objects.get(seriesID=series_id)
    serie.users.remove(user)
    return HttpResponse("Sikeres leiratkozás")


@login_required
def my_series(request):
    """Visszakapjuk azokat a sorozatokat amelyekre fel vagyunk iratkozva. Használatához bejelentkezés szükséges."""
    series_set = SeriesTable.objects.filter(users__username=request.user.username)
    data = []
    series_id = []
    pool = ThreadPool(processes=10)
    threads = []
    for serie in series_set:
        threads.append(pool.apply_async(search_tv_by_id, [serie.seriesID]))
        series_id.append(serie.seriesID)

    for i in threads:
        data.append(i.get())

    return render(request, "series/my-series.html", {"series": data})


@login_required
def my_profile(request):
    """Saját proflunk adatait jeleníti meg. Használatához bejelentkezés szükséges."""
    user = User.objects.get(username=request.user.username)
    error_msg = ""
    if request.method == "POST":
        if "email" in request.POST and request.POST["email"] != "":
            user.email = request.POST["email"]
        if "pw1" in request.POST and "pw2" in request.POST and request.POST["pw1"] == request.POST["pw2"] and request.POST["pw1"] != "":
            user.set_password(request.POST["pw1"])
        elif "pw1" in request.POST and request.POST["pw1"] != "":
            error_msg = "A két jelszó nem egyezik meg"

        if "emailNotify" in request.POST:
            user.emailNotify = True
        else:
            user.emailNotify = False
        user.save()

    data = {"username": user.username, "email": user.email, "emailNotify": user.emailNotify, "profileerror": error_msg}

    return render(request, "series/myprofile.html", data)


def get_hint(request, title):
    """Ha elkezdjük gépelni a sorozat címét a keresőbe, ennek a függvénynek a segítségével kapjuk vissza a tippeket."""
    # létrehozza a kapcsolatot
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"

    # összefűzzük a linket a lekérdezéshez
    link = "/3/search/tv?"
    link += urllib.parse.urlencode({"query": title, "language": language, "api_key": api_key})

    # meghívja a linket és a visszakapott JSON-t eltárolja a data változóban
    conn.request("GET", link, payload)
    res = conn.getresponse()
    data = res.read()
    return HttpResponse(data.decode("utf-8"))


def search_tv_by_id(id):
    """Sorozatokra tudunk keresni id alapján. A sorozat id-ját, címét, értékelését, első megjelenés dátumát,
     következő epizód dátumát és a rövid leírást adja meg a sorrozatról.
    Az id a bemenő paraméter. A dátumokat formázott stringként adja vissza."""
    # létrehozza a kapcsolatot
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"

    link = "/3/tv/" + str(id) + "?"
    link += urllib.parse.urlencode({"api_key": api_key, "language": language})
    conn.request("GET", link, payload)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    last_season_num = json_data["seasons"][len(json_data["seasons"]) - 1]["season_number"]

    output_data = {"id": id, "name": json_data["name"], "first_air_date": json_data["first_air_date"],
                   "next_episode_date": "Ismeretlen"}

    # Ha az utolsó évad üres, akkor megnézi az egyel korábbi évadot, de optimalizálási
    # okok miatt csak az egyel korábbit, ha nem az első évadról van szó
    first_search = True
    while first_search or output_data["next_episode_date"] == -1:
        # Csökkentsük az évadszámot, ha az utolsó üres volt és nem az első évadról van szó
        if output_data["next_episode_date"] == -1 and last_season_num > 1:
            last_season_num -= 1
        # Első évad esetén csak adjunk Ismeretlen-t és lépjünk ki a ciklusból
        elif output_data["next_episode_date"] == -1:
            output_data["next_episode_date"] = "Ismeretlen"
            break

        link = "/3/tv/" + str(id) + "/season/" + str(last_season_num) + "?"
        link += urllib.parse.urlencode({"api_key": api_key, "language": language})
        conn.request("GET", link, payload)
        res = conn.getresponse()
        data = res.read()
        json_data = json.loads(data.decode("utf-8"))

        # formázott stringként adja vissza a dátumot
        today = datetime.datetime.today().strftime("%Y-%m-%d")

        # Ellenőrizzük hogy a lekérdezett évad nem üres-e
        if len(json_data["episodes"]) != 0:
            for i in json_data["episodes"]:
                if i["air_date"] >= today:
                    output_data["next_episode_date"] = i["air_date"]
                    break
        # Ha üres és ez volt az első keresés, akkor -1 el újrakezdjük a ciklust
        elif first_search:
            output_data["next_episode_date"] = -1
        first_search = False

    return output_data


def search_tv(title):
    """Sorozatokra tudunk keresni cím alapján. A sorozat id-ját, címét, értékelését, első megjelenés dátumát,
     következő epizód dátumát és a rövid leírást adja meg a sorrozatról.
    A cím a bemenő paraméter. A dátumokat formázott stringként adja vissza."""
    # létrehozza a kapcsolatot
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"

    # összefűzzük a linket a lekérdezéshez
    link = "/3/search/tv?"
    link += urllib.parse.urlencode({"query": title, "language": language, "api_key": api_key})

    # meghívja a linket és a visszakapott JSON-t eltárolja a data változóban
    conn.request("GET", link, payload)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    output_data = {
        "id": json_data["results"][0]["id"],
        "name": json_data["results"][0]["name"],
        "vote_average": str(json_data["results"][0]["vote_average"]),
        "first_air_date": json_data["results"][0]["first_air_date"],
        "next_episode_date": "Ismeretlen",
        "overview": json_data["results"][0]["overview"]
    }
    id = json_data["results"][0]["id"]
    tv_data = search_tv_by_id(id)
    output_data["next_episode_date"] = tv_data["next_episode_date"]

    return output_data


def search_movie(title):
    """Filmekre tudunk keresni cím alapján. A cím a bemenő paraméter. A film id-ját, címét, értékelését,
     első megjelenés dátumát és a rövid leírást adja meg a sorrozatról."""
    # létrehozza a kapcsolatot
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"

    # összefűzzük a linket a lekérdezéshez
    link = "/3/search/movie?"
    link += urllib.parse.urlencode({"query": title, "language": language, "api_key": api_key})

    # meghívja a linket és a visszakapott JSON-t eltárolja a data változóban
    conn.request("GET", link, payload)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    output_data = {
        "id": json_data["results"][0]["id"],
        "name": json_data["results"][0]["title"],
        "vote_average": str(json_data["results"][0]["vote_average"]),
        "first_air_date": json_data["results"][0]["release_date"],
        "next_episode_date": "Ismeretlen",
        "overview": json_data["results"][0]["overview"]
    }

    return output_data
