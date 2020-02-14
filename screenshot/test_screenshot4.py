#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://funmatu.wordpress.com/2017/06/01/pyautogui%EF%BC%9Fpywinauto%EF%BC%9F/

import win32gui
import win32ui
import win32con
from PIL import Image
 


import win32gui
import win32api
import win32ui
import win32con
 
# スクリーン全体
hwnd = win32gui.GetDesktopWindow()
SM_XVIRTUALSCREEN = 76
SM_YVIRTUALSCREEN = 77
SM_CXVIRTUALSCREEN = 78
SM_CYVIRTUALSCREEN = 79
w = vscreenwidth = win32api.GetSystemMetrics(SM_CXVIRTUALSCREEN)
h = vscreenheigth = win32api.GetSystemMetrics(SM_CYVIRTUALSCREEN)
l = vscreenx = win32api.GetSystemMetrics(SM_XVIRTUALSCREEN)
t = vscreeny = win32api.GetSystemMetrics(SM_YVIRTUALSCREEN)
r = l + w
b = t + h
 
hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()
 
saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
saveDC.SelectObject(saveBitMap)
saveDC.BitBlt((0, 0), (w, h),  mfcDC,  (l, t),  win32con.SRCCOPY)
saveBitMap.SaveBitmapFile(saveDC, 'test_shot90.bmp')

bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)
img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
img.save('test_shot91.png')

# マウス位置キャプチャ
hwnd = win32gui.WindowFromPoint(win32gui.GetCursorPos())
w0, h0, w1, h1 = win32gui.GetWindowRect(hwnd)
 
hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()
 
saveBitMap = win32ui.CreateBitmap()
saveBitMap.CreateCompatibleBitmap(mfcDC, w1-w0, h1-h0)
saveDC.SelectObject(saveBitMap)
saveDC.BitBlt((0, 0), (w1-w0, h1-h0),  mfcDC,  (0, 0),  win32con.SRCCOPY)
bmpinfo = saveBitMap.GetInfo()
bmpstr = saveBitMap.GetBitmapBits(True)
img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
img.save('test_shot92.png')


