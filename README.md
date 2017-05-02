# Finding Ubike


Finding Ubike is a RESTful api which can find two nearest non-empty ubike station from your location(lat/lng).  

For example: 
The Latitude and longitude of Taipei101 is (25.034020, 121.564467)  
+ https://django-boy.herokuapp.com/v1/ubike-station/taipei/?lat=25.034020&lng=121.564467

will return a Response:
+ {"code": 0, "result": [{"station": "世貿二館", "num_ubike": "19"}, {"station": "世貿三館", "num_ubike": "22"}]}

## "code":
+ 1: all ubike stations are full
+ 0: OK
+ -1: invalid latitude or longitude
+ -2: given location not in Taipei City
+ -3: system error
## "result":
+ return empty list as result while returning non-zero code.



# Reference

1. YouBike臺北市公共自行車即時資訊
http://data.taipei/opendata/datalist/datasetMeta?oid=8ef1626a-892a-4218-8344-f7ac46e1aa48
2. Google Maps Geocoding API
https://developers.google.com/maps/documentation/geocoding/start?hl=zh-tw
3. Getting Started on Heroku with Python
https://devcenter.heroku.com/categories/python
4. DOKELUNG'S BLOG
http://dokelung-blog.logdown.com/posts/220274-django-note-1-building-and-settings