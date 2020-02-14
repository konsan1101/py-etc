#!/usr/bin/env python
# -*- coding: utf-8 -*-

# http://e-yuki67.hatenablog.com/entry/2017/02/12/152759

import os
import numpy as np
import cv2

if (os.name == 'nt'):
    import ctypes
    user32 = ctypes.windll.user32
    SCREEN_WIDTH  = user32.GetSystemMetrics(78)
    SCREEN_HEIGHT = user32.GetSystemMetrics(79)

    import win32gui
    import win32ui
    import win32con
    from PIL import Image

class win_shot_class:

    def __init__(self, ):
        pass
    
    def screenshot(self, ):
        window = win32gui.GetDesktopWindow()
        window_dc = win32ui.CreateDCFromHandle(win32gui.GetWindowDC(window))
        compatible_dc = window_dc.CreateCompatibleDC()

        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(window_dc, SCREEN_WIDTH, SCREEN_HEIGHT)
        compatible_dc.SelectObject(bmp)
        compatible_dc.BitBlt((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), window_dc, (0, 0), win32con.SRCCOPY)
        pil_img = Image.frombuffer('RGB', (SCREEN_WIDTH, SCREEN_HEIGHT), bmp.GetBitmapBits(True), 'raw', 'BGRX', 0, 1)

        window = None
        window_dc = None
        compatible_dc = None
        bmp = None
        return pil_img



if __name__ == '__main__':

    win_shot = win_shot_class()
    frm = win_shot.screenshot()
    frame = np.asarray(frm, dtype=np.uint8)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    cv2.imshow("", frame)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


    