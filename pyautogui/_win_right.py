#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://pyautogui.readthedocs.io/en/latest/keyboard.html

import pyautogui

pyautogui.keyDown('ctrlleft')
pyautogui.keyDown('winleft')

pyautogui.keyDown('right')
pyautogui.keyUp('right')

pyautogui.keyUp('winleft')
pyautogui.keyUp('ctrlleft')


