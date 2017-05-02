# -*- coding: utf8 -*-

from django.test import TestCase

import json
import requests
import re
import urllib
import gzip
from django.http import JsonResponse
# Create your tests here.
try:
    float("hi")
except ValueError:
    print("not a value!")

lat, lng = 0, 0

if not(-90<= lat <= 90 and -180 <= lng <= 180): # check lat/lng
    print("error")
else:
    print("do stuff")

def get_distance(loc1, loc2): # relative distance
    return sum(abs(l[0]-l[1])**2 for l in zip(loc1, loc2)) # norm(X1, X2)**2

def testJson(lat, lng):

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
        return json.dumps({"code": 0, "result": [
                    {
                        "station": s[0],
                        "num_ubike": s[1]
                    } for s in top_two
                ]
             } )


lat, lng = 25.034, 121.568
test_url = "https://p-demo.herokuapp.com/v1/ubike-station/taipei/?lat={}&lng={}".format(lat, lng)
r = requests.get(test_url)
print(r)
print(r.text)



