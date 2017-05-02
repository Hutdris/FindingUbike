from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext

import json
import requests
import os
import re
import urllib
import gzip

from .models import Greeting

#dirty functions
def in_taipei(lat, lng):
    googlemap_key = os.environ.get("GOOGLEMAP_API")
    googlemap_url = \
        "https://maps.googleapis.com/maps/api/geocode/json?latlng={_lat},{_lng}&key={key}".\
        format(_lat=lat, _lng=lng, key=googlemap_key)

    r = requests.get(googlemap_url)
    taipei = re.compile("Taipei City") # Prevent the empty result/ lots of ifelse
    for i in r.text.split('"'):
        if taipei.match(i):
            return True
    return False

def get_distance(loc1, loc2): # relative distance
    return sum(abs(l[0]-l[1])**2 for l in zip(loc1, loc2)) # norm(X1, X2)**2

def get_result(lat, lng):
    taipei_sarea = ["士林區", "北投區", "內湖區", "文山區", "南港區", "中山區"
        , "大安區", "信義區", "松山區", "萬華區", "中正區", "大同區"]

    url = "http://data.taipei/youbike"
    r = urllib.request.Request(url)
    response = urllib.request.urlopen(r)
    decompressed_data = gzip.decompress(response.read())
    r = json.loads(decompressed_data.decode("utf8"))

    print(r["retCode"])
    if r["retCode"] != 1:
        return json.dumps({"code": 3, "result": []})
    valid_stations = []
    for i in r["retVal"].values():
        if i["sarea"] in taipei_sarea and int(i["sbi"]) > 0:
            valid_stations.append([i["sna"], i["sbi"], get_distance((lat, lng), [float(i) for i in (i["lat"], i["lng"])])])
    valid_stations = sorted(valid_stations, key=lambda x: x[-1])
    top_two = valid_stations[:min(2, len(valid_stations))]

    if len(top_two) == 0:
        return json.dumps({"code": 1, "result": []})
    else:
        print(top_two)
        return json.dumps({"code": 0, "result": [
                    {
                        "station": s[0],
                        "num_ubike": s[1]
                    } for s in top_two
                ]
             }, ensure_ascii=False)

    # keep the neras
# Create your views here.
def index(request):

    return JsonResponse({"code": -1, "result": []})



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def search(request):

    if not all(tag in request.GET for tag in ("lat", "lng")):
        print("invalid url")
        return JsonResponse({"code": -1, "result": []})

    try:
        lat = float(request.GET["lat"])
        lng = float(request.GET["lng"])
    except ValueError:
        return JsonResponse({"code": -1, "result": []}) # invalid input

    if not(-90<= lat <= 90 and -180 <= lng <= 180):
        return JsonResponse({"code": -1, "result": []}) # invalid latitude or longitude

    if not in_taipei(lat, lng):
        return JsonResponse({"code": -2, "result": []}) # out of taipei city

    return HttpResponse(get_result(lat, lng), content_type='application/json', charset = 'cp950' )


