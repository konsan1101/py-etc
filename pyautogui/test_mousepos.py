#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui
import time

chkTime = time.time()
while ((time.time() - chkTime) < 30):
    x,y = pyautogui.position()
    if (x<100) and (y<100):
        pyautogui.moveTo(101,101)
    print(x,y)
    time.sleep(0.50)


