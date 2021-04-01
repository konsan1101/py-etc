#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui
import time
import datetime
import random

class proc_mousePointer:

    def __init__(self, ):
        print('pyautogui.FAILSAFE = False')
        time.sleep(1)
        pyautogui.FAILSAFE = False

        print('Change Sub Screen ...')
        time.sleep(1)
        pyautogui.keyDown('ctrlleft')
        pyautogui.keyDown('winleft')
        pyautogui.press('right')
        pyautogui.keyUp('winleft')
        pyautogui.keyUp('ctrlleft')

        print('Parameter Setting ...')
        time.sleep(1)
        self.waitSec= 60
        self.dayStart   = '06:55:00'
        self.dayEnd     = '16:05:00'
        self.lunchStart = '12:05:00'
        self.lunchEnd   = '12:55:00'

    def init(self, ):
        (w, h) = pyautogui.size()
        self.sc_width  = w
        self.sc_height = h
        print('screen', self.sc_width, self.sc_height)

        self.moveTo(self.sc_width / 2, self.sc_height / 2)
        self.last_t = time.time()
        self.startMsg = False

    def moveTo(self, x, y):
        try:
            pyautogui.moveTo(int(x), int(y))
        except Exception as e:
            pass
        try:
            pyautogui.press("ctrl")
        except Exception as e:
            pass

        (x, y) = pyautogui.position()
        self.last_x = x
        self.last_y = y

        print('position', self.last_x, self.last_y)

    def check(self, ):
        nowTime = datetime.datetime.now()
        nowHHMMSS = nowTime.strftime('%H:%M:%S')
        if (nowHHMMSS < self.dayStart) \
        or (nowHHMMSS > self.dayEnd):
            if (self.startMsg == True):
                self.startMsg = False
                print('mouse pointer stop')
            return
        if  (nowHHMMSS > self.lunchStart) \
        and (nowHHMMSS < self.lunchEnd):
            if (self.startMsg == True):
                self.startMsg = False
                print('mouse pointer stop')
            return

        (x, y) = pyautogui.position()
        if (x != self.last_x) or (y != self.last_y):
            if (self.startMsg == True):
                self.startMsg = False
                print('mouse pointer stop')

            self.last_x = x
            self.last_y = y
            self.last_t = time.time()

        if ((time.time() - self.last_t) > self.waitSec):
            if (self.startMsg == False):
                self.startMsg = True
                print('mouse pointer start')

            x += int(random.random() * 10) - 5
            if (x < 100):
                x = 100
            if (x > (self.sc_width-100)):
                x = (self.sc_width-100)
            y += int(random.random() * 10) - 5
            if (y < 100):
                y = 100
            if (y > (self.sc_height-100)):
                y = (self.sc_height-100)

            self.moveTo(x, y)



if __name__ == '__main__':

    mousePointer = proc_mousePointer()
    mousePointer.init()

    while True:
        mousePointer.check()
        time.sleep(10)


