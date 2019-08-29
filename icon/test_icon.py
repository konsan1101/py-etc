#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

img = Image.open('A-ZiP.png')
icon_sizes =[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256),]
img.save('A-ZiP.ico', size=icon_sizes)


