#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://www.robotech-note.com/entry/2016/12/21/213024

#from pygeocoder import Geocoder
#address = u'国会議事堂'
#results = Geocoder.geocode(address)
#print(results[0].coordinates)

#result = Geocoder.reverse_geocode(*results.coordinates, language="ja")
#print(result)

#http://vivo-design.blogspot.com/2011/06/google-map-apipythongooglemaps.html

#from googlemaps import GoogleMaps
import googlemaps as gm
gmaps = gm.googlemaps()
address = u'岡山市'
lat, lng = gmaps.address_to_latlng(address)
print(lat, lng)



