from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import http.client, urllib.parse, json, configparser, datetime, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read((os.path.join(BASE_DIR,  'conf.cnf'),))
if config.sections() == []:
    print("Nem sikerült beolvasni a conf.cnf fájlt. A program leáll...")
    exit(1)

api_key = config["SW"]["apiKey"]
language = config["SW"]["language"]


def index(request):
    if request.user.is_authenticated and isinstance(request.user, User):
        # TODO: Ez itt valamiért még mindig beadja anonym usernél...
        user = request.user.username
    else:
        user = "LOGIN"

    context = {"name": "", "vote_average": "", "first_air_date": "", "next_episode_date": "", "overview": ""}

    try:
        title = request.POST["title"]
        if title != "":
            context = search_tv(title)
    except KeyError:
        print("GET-el lett megnyitva az index.")
    except IndexError:
        try:
            context = search_movie(title)
        except IndexError:
            context["name"] = "Nincs ilyen film/sorozat"
    context["user"] = user
    return render(request, "series/index.html", context)


def login_view(request):
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
    logout(request)
    return redirect("index")


def register_view(request):
    try:
        user = request.POST["usrname-r"]
        email = request.POST["email-r"]
        pass1 = request.POST["pwd-r"]
        pass2 = request.POST["pwd-r2"]
        if pass1 != pass2:
            context = {"regerror": "A megadott jelszavak nem egyeznek meg."}
            return render(request, "series/index.html", context)
        else:
            try:
                dbuser = User.objects.get(username=user)  # Ha ez lefut, akkor már van ilyen user a db-ben
                context = {"regerror": "Már van ilyen nevű felhasználó: " + dbuser.username}
                return render(request, "series/index.html", context)
            except ObjectDoesNotExist:
                User.objects.create_user(user, email, pass1)
            return redirect("index")
    except KeyError:
        return redirect("index")


@login_required
def my_series(request):
    return render(request, "series/my-series.html", {})


def search_tv(title):
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
        "name": json_data["results"][0]["name"],
        "vote_average": str(json_data["results"][0]["vote_average"]),
        "first_air_date": json_data["results"][0]["first_air_date"],
        "next_episode_date": "Ismeretlen",
        "last_air_date": "Ismeretlen",
        "overview": json_data["results"][0]["overview"]
    }
    id = json_data["results"][0]["id"]

    link = "/3/tv/" + str(id) + "?" + urllib.parse.urlencode({"api_key": api_key, "language": language})
    conn.request("GET", link, payload)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    output_data["last_air_date"] = json_data["last_air_date"]
    last_season_num = json_data["seasons"][len(json_data["seasons"])-1]["season_number"]

    link = "/3/tv/" + str(id) + "/season/" + str(last_season_num) + "?"
    link += urllib.parse.urlencode({"api_key": api_key, "language": language})
    conn.request("GET", link, payload)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))

    today = datetime.datetime.today().strftime("%Y-%m-%d")  # formázott stringként adja vissza a dátumot
    print(link)
    for i in json_data["episodes"]:
        if i["air_date"] >= today:
            output_data["next_episode_date"] = i["air_date"]
            break

    print(str(output_data["next_episode_date"]))

    return output_data


def search_movie(title):
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
        "name": json_data["results"][0]["title"],
        "vote_average": str(json_data["results"][0]["vote_average"]),
        "first_air_date": json_data["results"][0]["release_date"],
        "next_episode_date": "Ismeretlen",
        "last_air_date": "Ismeretlen",
        "overview": json_data["results"][0]["overview"]
    }

    return output_data
