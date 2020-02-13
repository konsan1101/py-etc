#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui         

s = pyautogui.screenshot()
s.save('test_shot1.jpg')

import ctypes
user32 = ctypes.windll.user32
x,y  = user32.GetSystemMetrics(78), user32.GetSystemMetrics(79)

s = pyautogui.screenshot(region=(0,0,x,y))
s.save('test_shot2.jpg')


