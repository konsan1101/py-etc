#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui
import time

x,y = pyautogui.position()

chkTime = time.time()
while ((time.time() - chkTime) < 60):
    new_x,new_y = pyautogui.position()
    if (new_x != x) or (new_y != y):
        x,y = new_x,new_y
        print(x,y)
    time.sleep(0.50)


