#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2023 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import os
import time

import screeninfo
import pyautogui
if (os.name == 'nt'):
    import ctypes

import array

import pyperclip



class qGUI_class:

    def __init__(self, ):
        print('pyautogui.FAILSAFE = False')
        pyautogui.FAILSAFE = False

        # 初期化
        self.screen_count  = -1
        self.screen_name   = {}
        self.screen_left   = {}
        self.screen_top    = {}
        self.screen_width  = {}
        self.screen_height = {}
        self.screen_mouseX = {}
        self.screen_mouseY = {}

        # プライマリ
        for s in screeninfo.get_monitors():
            if (s.is_primary == True):
                #print(str(s))
                if (self.screen_count < 0):
                    self.screen_count = 0
                self.screen_name[  self.screen_count] = s.name
                self.screen_left[  self.screen_count] = s.x
                self.screen_top[   self.screen_count] = s.y
                self.screen_width[ self.screen_count] = s.width
                self.screen_height[self.screen_count] = s.height
                self.screen_mouseX[self.screen_count] = 0
                self.screen_mouseY[self.screen_count] = 0
                self.screen_count += 1
        # サブ
        for s in screeninfo.get_monitors():
            if (s.is_primary == False):
                #print(str(s))
                if (self.screen_count < 0):
                    self.screen_count = 0
                self.screen_name[  self.screen_count] = s.name
                self.screen_left[  self.screen_count] = s.x
                self.screen_top[   self.screen_count] = s.y
                self.screen_width[ self.screen_count] = s.width
                self.screen_height[self.screen_count] = s.height
                self.screen_mouseX[self.screen_count] = 0
                self.screen_mouseY[self.screen_count] = 0
                self.screen_count += 1

    def init(self, ):
        pass



    def size(self, ):
        return pyautogui.size()
    def position(self, ):
        return pyautogui.position()
    def moveTo(self, x=0, y=0, ):
        return pyautogui.moveTo(int(x), int(y))
    def keyDown(self, s='', ):
        return pyautogui.keyDown(s)
    def keyUp(self, s='', ):
        return pyautogui.keyUp(s)
    def press(self, s='', ):
        return pyautogui.press(s)
    def screenshot(self, ):
        return pyautogui.screenshot()



    def movePointer(self, left=0, top=0, offset=False, click=None, ):
        if (offset == False):
            X = left
            Y = top
            pyautogui.moveTo(x=X, y=Y, )
            if (not click is None):
                pyautogui.click(x=X, y=Y, clicks=1, interval=0.5, button=click)
            return True
        else:
            X, Y = pyautogui.position()
            X = int(X + left)
            Y = int(Y + top)
            pyautogui.moveTo(x=X, y=Y, )
            if (not click is None):
                pyautogui.click(x=X, y=Y, clicks=1, interval=0.5, button=click)
            return True

    def sendKey(self, txt='', cr=True, lf=False, afterSec=0, ):
        out_txt = txt
        if (cr==True) or (lf==True):
            out_txt = out_txt.replace('\r', '')
            out_txt = out_txt.replace('\n', '')
        pyperclip.copy(out_txt)
        pyautogui.hotkey('ctrl', 'v')
        if (cr==True) or (lf==True):
            pyautogui.typewrite(['enter',])
        if (afterSec != 0):
            time.sleep(afterSec)
        return True

    def keyPress(self, keys=[], afterSec=0, ):
        for key in keys:
            pyautogui.press(key)
            if (afterSec != 0):
                time.sleep(afterSec)
        return True

    def checkImageHit(self, filename='', confidence=0.9, waitSec=5, movePointer=True, ):
        left   = 0
        top    = 0
        width  = 0
        height = 0
        if (filename==''):
            return False, left, top, width, height
        chktime = time.time()
        res = pyautogui.locateOnScreen(filename, confidence=confidence, )
        while (res == None) and ((time.time() - chktime) < waitSec):
            time.sleep(0.10)
            res = pyautogui.locateOnScreen(filename, confidence=confidence, )
        if (res is None):
            return False, left, top, width, height
        else:
            left   = res[0]
            top    = res[1]
            width  = res[2]
            height = res[3]
            if (movePointer == True):
                pyautogui.moveTo(x=int(left+width/2), y=int(top+height/2), )
            return True, left, top, width, height

    def checkImageHide(self, filename='', confidence=0.9, waitSec=5, ):
        if (filename==''):
            return True
        chktime = time.time()
        res = pyautogui.locateOnScreen(filename, confidence=confidence, )
        while (not res is None) and ((time.time() - chktime) < waitSec):
            time.sleep(0.10)
            res = pyautogui.locateOnScreen(filename, confidence=confidence, )
        if (res is None):
            return True
        else:
            return False

    def getPanelPos(self, panel='0-', ):
        #left, top, width, height = getPanelPos(panel,)
        return self.getScreenPanelPosSize(screen=0, panel=panel, )

    def getResolution(self, reso='full', ):
        if (reso == 'full')  \
        or (reso == 'full+') \
        or (reso == 'full-'):
            left, top, width, height = self.getScreenPosSize(screen=0, )
            if (width == None):
                width  = 1200
                height = 720

        if   (reso == 'full'): 
            return width, height
        if   (reso == 'full+'):
            return width + 90, height + 50
        if   (reso == 'full-'):
            return int(width*0.9), int(height*0.9)
        elif (reso == 'half'):
            return int(width/2), int(height/2)

        elif (reso=='4k'):
                return 3840,2160
        elif (reso=='2k') or (reso=='hdtv'):
                return 1920,1080
        elif (reso=='fhd') or (reso=='1920x1080'):
                return 1920,1080
        elif (reso=='uxga'):
                return 1600,1200
        elif (reso=='hd') or (reso=='1366x768'):
                return 1366,768
        elif (reso=='720p') or (reso=='1280x720'):
                return 1280,720
        elif (reso=='xga') or (reso=='1024x768'):
                return 1024,768
        elif (reso=='svga') or (reso=='800x600'):
                return 800,600
        elif (reso=='dvd'):
                return 720,480
        elif (reso=='vga') or (reso=='640x480'):
                return 640,480
        elif (reso=='qvga') or (reso=='320x240'):
                return 320,240
        elif (reso=='160x120'):
                return 160,120
        print('getResolution error ' + reso + ', -> 640,480')
        return 640,480



    def getCornerScreen(self, rightLeft='right', topBottom='top', ):
        screen = 0
        x = None
        y = None
        # 右左で最大最高値求める
        for s in range(self.screen_count):
            if (rightLeft.lower() == 'right'):
                wx = self.screen_left[s] + self.screen_width[s] 
                if (x == None):
                    x = wx
                elif (wx > x):
                    x = wx
            if (rightLeft.lower() == 'left'):
                wx = self.screen_left[s] 
                if (x == None):
                    x = wx
                elif (wx < x):
                    x = wx
        # 右左の最大最小値で、上下最大最小値の場所を求める
        for s in range(self.screen_count):
            if (rightLeft.lower() == 'right'):
                if (self.screen_left[s] + self.screen_width[s] == x): 
                    if (topBottom.lower() == 'top'):
                        wy = self.screen_top[s] 
                        if (y == None):
                            y = wy
                            screen = s
                        elif (wy < y):
                            y = wy
                            screen = s
                    if (topBottom.lower() == 'bottom'):
                        wy = self.screen_top[s] + self.screen_height[s] 
                        if (y == None):
                            y = wy
                            screen = s
                        elif (wy > y):
                            y = wy
                            screen = s
            if (rightLeft.lower() == 'left'):
                if (self.screen_left[s] == x): 
                    if (topBottom.lower() == 'top'):
                        wy = self.screen_top[s] 
                        if (y == None):
                            y = wy
                            screen = s
                        elif (wy < y):
                            y = wy
                            screen = s
                    if (topBottom.lower() == 'bottom'):
                        wy = self.screen_top[s] + self.screen_height[s] 
                        if (y == None):
                            y = wy
                            screen = s
                        elif (wy > y):
                            y = wy
                            screen = s
        return screen

    def getScreenPosSize(self, screen=0, ):
        if (screen > (self.screen_count-1)):
            return None, None, None, None
        left   = self.screen_left[  screen]
        top    = self.screen_top[   screen]
        width  = self.screen_width[ screen]
        height = self.screen_height[screen]
        return left, top, width, height

    def getScreenPanelPosSize(self, screen=0, panel='0-', ):
        #left, top, width, height = getScreenPanelPosSize(screen, panel,)

        l, t, w, h = self.getScreenPosSize(screen=screen, )
        if (l == None):
            return None, None, None, None

        wa = int(w/100) 
        ha = int(h/100) 
        wb = int(w/20) 
        hb = int(h/20) 

        if   (panel == '0'):
            return l+0, t+0, w, h
        elif (panel == '0-'):
            return l+wb, t+hb, int(w-wb*2), int(h-hb*2)
        elif (panel == '0+'):
            return l-30, t-30, w+60, h+60
        elif (panel == '1'):
            return l+0, t+0, int(w/3), int(h/3)
        elif (panel == '1-'):
            return l+wa, t+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (panel == '2'):
            return l+int(w/3), t+0, int(w/3), int(h/3)
        elif (panel == '2-'):
            return l+int(w/3)+wa, t+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (panel == '3'):
            return l+w-int(w/3), t+0, int(w/3), int(h/3)
        elif (panel == '3-'):
            return l+w-int(w/3)+wa, t+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (panel == '4'):
            return l+0, t+int(h/3), int(w/3), int(h/3)
        elif (panel == '4-'):
            return l+wa, t+int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (panel == '5'):
            return l+int(w/3), t+int(h/3), int(w/3), int(h/3)
        elif (panel == '5-'):
            return l+int(w/3)+wa, t+int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (panel == '5+'):
            return l+int(w/4), t+int(h/4), int(w/2), int(h/2)
        elif (panel == '6'):
            return l+w-int(w/3), t+int(h/3), int(w/3), int(h/3)
        elif (panel == '6-'):
            return l+w-int(w/3)+wa, t+int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (panel == '7'):
            return l+0, t+h-int(h/3), int(w/3), int(h/3)
        elif (panel == '7-'):
            return l+wa, t+h-int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (panel == '8'):
            return l+int(w/3), t+h-int(h/3), int(w/3), int(h/3)
        elif (panel == '8-'):
            return l+int(w/3)+wa, t+h-int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (panel == '9'):
            return l+w-int(w/3), t+h-int(h/3), int(w/3), int(h/3)
        elif (panel == '9-'):
            return l+w-int(w/3)+wa, t+h-int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (panel == '1t'):
            return l+wb, t+hb, int(w/3), int(h/10)
        elif (panel == '123t'):
            return l+0, t+0, w, int(h/5)
        elif (panel == '456t'):
            return l+0, t+int(h*0.4), w, int(h/5)
        elif (panel == '789t'):
            return l+0, t+h-int(h/5), w, int(h/5)
        else:
            return l+int(w/4), t+int(h/4), int(w/2), int(h/2)

    def screenPosition(self, screen=0, ):
        res = None
        (x, y) = pyautogui.position()
        for s in range(self.screen_count):
            if  (x >= self.screen_left[s]) \
            and (x <= self.screen_left[s]+self.screen_width[s]) \
            and (y >= self.screen_top[s]) \
            and (y <= self.screen_top[s]+self.screen_height[s]):
                self.screen_mouseX[s] = x - self.screen_left[s]
                self.screen_mouseY[s] = y - self.screen_top[s]
                res = s
        return (self.screen_mouseX[screen], self.screen_mouseY[screen]) , res

    def screenMoveTo(self, screen=0, x=0, y=0, ):
        screen_x = self.screen_left[screen] + x
        screen_y = self.screen_top[screen] + y
        return pyautogui.moveTo(int(screen_x), int(screen_y))



    def findWindow(self, winTitle='Display', ):
        if (os.name != 'nt'):
            return False
        parent_handle = ctypes.windll.user32.FindWindowW(0, winTitle)
        if (parent_handle == 0):
            return False
        else:
            return parent_handle

    def moveWindowSize(self, winTitle='Display', posX=0, posY=0, dspMode='full+', ):
        if (os.name != 'nt'):
            return False
        parent_handle = self.findWindow(winTitle)
        if (parent_handle == False):
            return False
        else:
            dspWidth, dspHeight = self.getResolution(dspMode)
            HWND_TOP = 0
            SWP_SHOWWINDOW = 0x0040
            ctypes.windll.user32.SetWindowPos(parent_handle, HWND_TOP, posX, posY, dspWidth, dspHeight, SWP_SHOWWINDOW)
            return True

    def setForegroundWindow(self, winTitle='Display', ):
        if (os.name != 'nt'):
            return False
        parent_handle = self.findWindow(winTitle)
        if (parent_handle == False):
            return False
        else:
            ctypes.windll.user32.SetForegroundWindow(parent_handle)
            return True



    def notePad(self, txt='', cr=True, lf=False, ):
        if (os.name != 'nt'):
            return False

        winTitle  = u'無題 - メモ帳'
        parent_handle = ctypes.windll.user32.FindWindowW(0, winTitle)
        if (parent_handle == 0):
            winTitle  = u'*無題 - メモ帳'
            parent_handle = ctypes.windll.user32.FindWindowW(0, winTitle)
            if (parent_handle == 0):
                return False

        out_txt = txt
        if (cr==True) or (lf==True):
            out_txt = out_txt.replace('\r', '')
            out_txt = out_txt.replace('\n', '')
        if (cr==True):
            out_txt += '\r'
        if (lf==True):
            out_txt += '\n'

        if (True):
        #try:
            child_handles = array.array('i')
            ENUM_CHILD_WINDOWS = ctypes.WINFUNCTYPE( \
                                ctypes.c_int, \
                                ctypes.c_int, \
                                ctypes.py_object)
            ctypes.windll.user32.EnumChildWindows( \
                                parent_handle, \
                                ENUM_CHILD_WINDOWS(self.enum_child_windows_proc), \
                                ctypes.py_object(child_handles) )
            WM_CHAR = 0x0102
            for i in range(len(out_txt)):
                ctypes.windll.user32.SendMessageW(child_handles[0], WM_CHAR, (ord(out_txt[i])), 0)
            return True
        #except Exception as e:
        #    return False

    def enum_child_windows_proc(self, handle, list):
        list.append(handle)
        return 1



if __name__ == '__main__':

    qGUI = qGUI_class()

    qGUI.init()

    for s in range(qGUI.screen_count):
        print(s, qGUI.getScreenPosSize(s))

    for s in range(qGUI.screen_count):
        print(s, qGUI.getScreenPanelPosSize(s,'5'))

    print('screen=0 mouse check 15s')
    x,y,s = 0,0,0
    chkTime = time.time()
    while ((time.time() - chkTime) < 15):
        (new_x, new_y), new_s = qGUI.screenPosition(screen=0)
        if (new_x != x) or (new_y != y):
            x,y = new_x,new_y
            print(x,y)
        if (new_s != s):
            s = new_s
            print('screen',s)
        time.sleep(0.50)

    x,y = qGUI.getResolution('full')
    print('getResolution x,y = ', x, y, )

    qGUI.notePad(txt=u'開始')
    ##qGUI.sendKey(txt=u'日本語')
    ##qGUI.sendKey(txt=u'abcdefg',lf=False)
    qGUI.notePad(txt=u'終了')



# ---------------
# pyautogui press
# ---------------
# Enterキー  ‘enter’,’retuen’,’\n’
# Escキー    ‘esc’
# Shiftキー  ‘shiftleft’,’shiftright’
# Altキー    ‘altleft’,’altright’
# Ctrlキー   ‘ctrlleft’,’ctrlright’
# Tabキー    ‘tab’,’\t’
# Backspaceキー・Deleteキー  ‘backspace’,’delete’
# PageUpキー・PageDownキー   ‘pageup’,’pagedown’
# Homeキー・Endキー          ‘Home’,’end’
# 矢印キー(↑↓←→)             ‘up’,’down’,’left’,’right’
# ファンクションキー          ‘f1′,’f2’,’f3’など
# 音量コントロールキー        ‘volumeup’,’volumedown’,’volumemute’
# Pauseキー      ‘pause’
# CapsLockキー   ‘capslock’
# NumLockキー    ‘numlock’
# ScrollLockキー ‘scrolllock’
# Insキー        ‘insert’
# PrintScreenキー‘printscreen’
# Winキー(Windowsのみ)   ‘winleft’,’winright’
# Commandキー(Macのみ)   ‘command’
# Optionキー(Macのみ)    ‘option’



