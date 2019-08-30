#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image

# white color to trans
img = Image.open('input.png')
alpha = img.split()[3]
img = img.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)
img.paste(255, mask)
img.save('output_gif.gif', transparency=0)

# gif to icon
icon_sizes =[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256),]

img = Image.open('output_gif.gif')
img.save('output_icon.ico', size=icon_sizes, )


