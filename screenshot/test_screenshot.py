#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes

user32 = ctypes.windll.user32
x,y  = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

import pyautogui

s = pyautogui.screenshot()
s.save('test_shot1.jpg')

s = pyautogui.screenshot(region=(0,0,x,y))
s.save('test_shot2.jpg')

from PIL import ImageGrab

img = ImageGrab.grab()
img.save('test_shot3.jpg')

img = ImageGrab.grab(bbox=(0, 0, x, y))
img.save('test_shot4.jpg')


