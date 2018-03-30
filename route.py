
KEY = "AIzaSyB1mfNCMMsONkubGOCkM64a1PzGDwEiNaA"

import requests
from gmplot import gmplot

response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA&key='+KEY)
gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 13)
resp_json_payload = response.json()

print(resp_json_payload['results'][0]['geometry']['location'])
lats, lons = zip(*[(resp_json_payload['results'][0]['geometry']['location']['lat'], resp_json_payload['results'][0]['geometry']['location']['lng'])])
gmap.plot(lats, lons, 'cornflowerblue', edge_width=10)