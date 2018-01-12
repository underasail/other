#! /usr/bin/python3

import requests
import gmplot

route_lats = []
route_lons = []

# https://console.developers.google.com/apis/credentials?project=mp-ice-routes
# http://www.indjango.com/google-api-to-get-lat-long-data/
address = input('Address to search routes for: ')
api_key = 'AIzaSyCkdlRImErGdlbI3KpJmqrP_yF2cIKRIXw'
gmaps_output = requests.get(\
'https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'\
.format(address, api_key))
gmaps_dict = gmaps_output.json()
if gmaps_dict['status'] == 'OK':
    gmaps_latitude = str(gmaps_dict['results'][0]['geometry']['location']['lat'])
    gmaps_longitude = str(gmaps_dict['results'][0]['geometry']['location']['lng'])

# https://www.mountainproject.com/data
url = 'https://www.mountainproject.com/data/'

module = 'get-routes-for-lat-lon' + '?'
lat = 'lat=' + gmaps_latitude +'&'
lon = 'lon=' + gmaps_longitude +'&'
maxDistance = 'maxDistance=' + \
input('Distance from coordinates to search (Miles <= 200): ') +'&'
maxResults = 'maxResults=' + '500' +'&'
key = 'key=' + '111385011-0baf40d3c2e2832ce026795faf0aebb0'

url = url + module + lat + lon + maxDistance + maxResults + key

# https://www.mountainproject.com/data/get-routes-for-lat-lon?\
# lat=44.155491&lon=-71.366258&maxDistance=1&key=111385011-0baf4\
# 0d3c2e2832ce026795faf0aebb0
webpage = requests.get(url)
routedata = webpage.json()['routes']
while len(routedata) == 500:
    print('Choose a smaller distance to see all routes in the area.')
    maxDistance = 'maxDistance=' + \
    input('Distance from coordinates to search (Miles <= 200): ') +'&'
    url = url + module + lat + lon + maxDistance + maxResults + key
    webpage = requests.get(url)
    routedata = webpage.json()['routes']

names = input('Print route names? (y/n): ')
for entry in routedata:
    route_lats.append(entry['latitude'])
    route_lons.append(entry['longitude'])
    if 'y' or 'Y' in names:
        print('%s: %s (%s, %s)' % (entry['name'], entry['type'], \
        entry['longitude'], entry['latitude']))

# https://github.com/vgm64/gmplot/blob/master/README.rst
# Had to edit apikey in line 18 of C:\Users\Thompson\AppData\
# Local\rodeo\app-2.5.2\resources\conda\Lib\site-packages\gmplot\gmplot.py
# to include the api_key listed above in this script

gmap = gmplot.GoogleMapPlotter.from_geocode(address, zoom = 10)
gmap.heatmap(route_lats, route_lons)
gmap.draw('C:\\Users\Thompson\Downloads\mymap.html')
