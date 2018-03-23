from django.shortcuts import render
import http.client, urllib.parse, json

api_key = "minta1"
language = "hu-HU"
page_number = 1


def index(request):
    try:
        title = request.POST['title']
        if title == "":
            context = {"name": "", "vote_average": "", "first_air_date": "", "overview": ""}
        else:
            context = search_tv(title)
    except KeyError:
        context = {"name": "", "vote_average": "", "first_air_date": "", "overview": ""}
    return render(request, 'series/index.html', context)


def search_tv(title):
    # létrehozza a kapcsolatot
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    payload = "{}"

    # összefűzzük a linket a lekérdezéshez
    link = "/3/search/tv?"
    link += urllib.parse.urlencode({"page": page_number, "query": title,
                                    "language": language, "api_key": api_key})

    # meghívja a linket és a visszakapott JSON-t eltárolja a data változóban
    conn.request("GET", link, payload)
    res = conn.getresponse()
    data = res.read()
    json_data = json.loads(data.decode("utf-8"))
    output_data = {
        "name": json_data["results"][0]["name"],
        "vote_average": str(json_data["results"][0]["vote_average"]),
        "first_air_date": json_data["results"][0]["first_air_date"],
        "overview": json_data["results"][0]["overview"]
    }

    return output_data
