#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://pyautogui.readthedocs.io/en/latest/keyboard.html

import pyautogui
import pyperclip
import time

time.sleep(5)

pyautogui.typewrite('Hello world!\n')

time.sleep(2)

#pyautogui.typewrite(u'こんにちは！\n')
pyperclip.copy(u'こんにちは！\n')
pyautogui.hotkey('ctrl', 'v')

time.sleep(2)

pyautogui.keyDown('ctrlleft')
pyautogui.keyDown('winleft')

pyautogui.keyDown('right')
pyautogui.keyUp('right')
pyautogui.keyDown('left')
pyautogui.keyUp('left')

pyautogui.keyUp('winleft')
pyautogui.keyUp('ctrlleft')

time.sleep(2)
