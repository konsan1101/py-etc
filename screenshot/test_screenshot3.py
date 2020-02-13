#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://e-yuki67.hatenablog.com/entry/2017/02/12/152759


import ctypes
user32 = ctypes.windll.user32
SCREEN_WIDTH  = user32.GetSystemMetrics(78)
SCREEN_HEIGHT = user32.GetSystemMetrics(79)
SCREEN_SCALING_FACTOR = 1.0

import win32gui
import win32ui
import win32con
from PIL import Image
import numpy as np
import cv2

#SCREEN_WIDTH = 1920
#SCREEN_HEIGHT = 1080
#SCREEN_SCALING_FACTOR = 1.0

def nt_screenshot():
    try:
        window = win32gui.GetDesktopWindow()
        window_dc = win32ui.CreateDCFromHandle(win32gui.GetWindowDC(window))
        compatible_dc = window_dc.CreateCompatibleDC()
        width = SCREEN_WIDTH
        height = SCREEN_HEIGHT
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(window_dc, width, height)
        compatible_dc.SelectObject(bmp)
        compatible_dc.BitBlt((0, 0), (width, height), window_dc, (0, 0), win32con.SRCCOPY)
        pil_img = Image.frombuffer('RGB', (width, height), bmp.GetBitmapBits(True), 'raw', 'BGRX', 0, 1)
        cv2_img = np.array(pil_img, dtype=np.uint8)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
        return cv2_img
    except:
        return None



if __name__ == '__main__':


    img = screenshot()
    cv2.imshow("", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    