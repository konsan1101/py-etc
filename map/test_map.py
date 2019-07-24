#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://qiita.com/momota10/items/3b878f01d489a32e40c3


import folium

m = folium.Map(location=[35.681382, 139.76608399999998], zoom_start=12)

folium.Marker([35.658581, 139.745433], popup='Tokyo tower', icon=folium.Icon(color='blue')).add_to(m)
folium.Marker([35.710063, 139.8107], popup='Tokyo skytree', icon=folium.Icon(color='blue', icon='cloud')).add_to(m)

m.save(outfile="test_output_map.html")


