#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://pyautogui.readthedocs.io/en/latest/keyboard.html

import pyautogui

if __name__ == '__main__':

    pyautogui.FAILSAFE = False

    pyautogui.keyDown('ctrlleft')
    pyautogui.keyDown('winleft')

    pyautogui.keyDown('right')
    pyautogui.keyUp('right')

    pyautogui.keyUp('winleft')
    pyautogui.keyUp('ctrlleft')


