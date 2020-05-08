#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://pyautogui.readthedocs.io/en/latest/keyboard.html

import time

import pyautogui
import pyperclip

def sendKey(txt='', cr=True, lf=False ):
    out_txt = txt
    if (cr==True) or (lf==True):
        out_txt = out_txt.replace('\r', '')
        out_txt = out_txt.replace('\n', '')

    pyperclip.copy(out_txt)
    pyautogui.hotkey('ctrl', 'v')

    if (cr==True) or (lf==True):
        pyautogui.typewrite(['enter',])

    return True

if (__name__ == '__main__'):

    print('wait 10s')
    time.sleep(10.00)

    while True:
        pyautogui.keyDown('f11')
        pyautogui.keyUp('f11')
        time.sleep(3.00)


