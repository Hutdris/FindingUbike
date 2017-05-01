from django.shortcuts import render
from django.http import HttpResponse

import requests
import os

from .models import Greeting

# Create your views here.
def index(request):
    # #return HttpResponse('Hello from Python!')
    # return render(request, 'index.html')

    url_msg = str(request.__dict__)
    print(url_msg)
    print(request)
    hi = "hi"
    lat, lng = 25.034415, 121.568924
    googlemap_api = os.environ.get("GOOGLEMAP_API")
    googlemap_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={_lat},{_lng}&key={api}".\
        format(_lat=lat, _lng=lng, api=googlemap_api)
    #r = requests.get(googlemap_url)
    return HttpResponse("{}".format(url_msg))
    # return HttpResponse("<pre>{}<pre>".format(r.text))



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def search(request):
    # #return HttpResponse('Hello from Python!')
    # return render(request, 'index.html')

    url_msg = str(request.__dict__)
    print(url_msg)
    print(request)
    hi = "hi"
    lat, lng = 25.034415, 121.568924
    googlemap_api = os.environ.get("GOOGLEMAP_API")
    googlemap_url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={_lat},{_lng}&key={api}". \
        format(_lat=lat, _lng=lng, api=googlemap_api)
    #r = requests.get(googlemap_url)
    return HttpResponse("象山第一站讚讚讚！")
    # return HttpResponse("<pre>{}<pre>".format(r.text))

