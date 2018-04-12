from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import http.client, urllib.parse, json, configparser, datetime

config = configparser.ConfigParser()
config.read("conf.cnf")
if config.sections() == []:
    print("Nem sikerült beolvasni a conf.cnf fájlt. A program leáll...")
    exit(1)

api_key = config["SW"]["apiKey"]
language = config["SW"]["language"]


def index(request):
    try:
        title = request.POST['title']
        if title == "":
            context = {"name": "", "vote_average": "", "first_air_date": "", "next_episode_date": "", "overview": ""}
        else:
            context = search_tv(title)
    except KeyError:
        context = {"name": "", "vote_average": "", "first_air_date": "", "next_episode_date": "", "overview": ""}
    except IndexError:
        context = {"name": "Nincs ilyen sorozat", "vote_average": "", "first_air_date": "", "next_episode_date": "", "overview": ""}
    return render(request, 'series/index.html', context)


@login_required
def my_series(request):
    return render(request, 'series/my-series.html', {})


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
