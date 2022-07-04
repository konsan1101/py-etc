#!/usr/bin/env python
# -*- coding: utf-8 -*-

import win32gui
import time

while True:
    try:
        hWnd = win32gui.GetForegroundWindow()
        print(win32gui.GetWindowText(hWnd))
    except:
        pass
    time.sleep(1)

