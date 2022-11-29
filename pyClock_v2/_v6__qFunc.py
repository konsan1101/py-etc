#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2022 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import sys
import os
import time
import datetime
import codecs
import glob

import json

import queue
import threading
import subprocess

import psutil
import signal
import shutil

import ctypes
import array

import unicodedata
import pyautogui
import pyperclip
import numpy as np
import cv2

from PIL import Image
import io
if (os.name == 'nt'):
    import win32clipboard

import socket
qHOSTNAME = socket.gethostname().lower()



qPath_sounds    = '_sounds/'
qPath_icons     = '_icons/'
qPath_fonts     = '_fonts/'



class qFunc_class:

    def __init__(self, ):
        self.qScreenWidth  = 0
        self.qScreenHeight = 0

    def __del__(self, ):
        pass
                
    def init(self, ):
        return True

    def setNice(self, nice, ):
        try:
            p = psutil.Process()
            if   (nice == 'high'): # 優先度: 高
                p.nice(psutil.HIGH_PRIORITY_CLASS)
            elif (nice == 'above'): # 優先度: 通常以上
                p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
            elif (nice == 'normal'): # 優先度: 通常
                p.nice(psutil.NORMAL_PRIORITY_CLASS)
            elif (nice == 'below'): # 優先度: 通常以下
                p.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
            elif (nice == 'idol'): # 優先度: 低
                p.nice(psutil.IDLE_PRIORITY_CLASS)
            else: # 優先度: 通常
                p.nice(psutil.NORMAL_PRIORITY_CLASS)
        except:
            pass

    def getNice(self, ):
        try:
            p = psutil.Process()
            nice = p.nice()
            if   (nice == psutil.HIGH_PRIORITY_CLASS): # 優先度: 高
                return 'high'
            elif (nice == psutil.ABOVE_NORMAL_PRIORITY_CLASS): # 優先度: 通常以上
                return 'above'
            elif (nice == psutil.NORMAL_PRIORITY_CLASS): # 優先度: 通常
                return 'normal'
            elif (nice == psutil.BELOW_NORMAL_PRIORITY_CLASS): # 優先度: 通常以下
                return 'below'
            elif (nice == psutil.IDLE_PRIORITY_CLASS): # 優先度: 低
                return 'idol'
            else: # 優先度: 通常
                pass
        except:
            pass
        return 'normal'

    def getJson(self, json_path='_config/', json_file='test_key.json', ):
        json_dic = {}
        try:
            with codecs.open(json_path + json_file, 'r', 'utf-8') as r:
                json_dic = json.load(r)
            if (json_dic != {}):
                return True, json_dic
        except Exception as e:
            print('getJson error! ' + json_path + json_file)
        return False, {}

    def putJson(self, json_path='_config/', json_file='test_key.json', json_dic={}, ):
        try:
            w = codecs.open(json_path + json_file, 'w', 'utf-8')
            w.write(json.dumps(json_dic, indent=4, ensure_ascii=False, ))
            w.close()
            return True
        except Exception as e:
            print('putJson error! ' + json_path + json_file) 
        return False

    def makeDirs(self, ppath, remove=False, ):
        try:
            if (len(ppath) > 0):
                path=ppath.replace('\\', '/')
                if (path[-1:] != '/'):
                    path += '/'
                if (not os.path.isdir(path[:-1])):
                    os.makedirs(path[:-1])
                else:
                    if (remove != False):
                        files = glob.glob(path + '*')
                        for f in files:
                            if (remove == True):
                                try:
                                    self.remove(f)
                                except Exception as e:
                                    pass
                            if (str(remove).isdigit()):
                                try:
                                    nowTime   = datetime.datetime.now()
                                    fileStamp = os.path.getmtime(f)
                                    fileTime  = datetime.datetime.fromtimestamp(fileStamp)
                                    td = nowTime - fileTime
                                    if (td.days >= int(remove)):
                                        self.remove(f)
                                except Exception as e:
                                    pass

        except Exception as e:
            pass
        return True

    def kill(self, name, ):
        if (os.name == 'nt'):
            try:
                kill = subprocess.Popen(['taskkill', '/im', name + '.exe', '/f', ], \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                kill.wait()
                kill.terminate()
                kill = None
                return True
            except Exception as e:
                pass
        else:
            try:
                kill = subprocess.Popen(['pkill', '-9', '-f', name, ], \
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
                kill.wait()
                kill.terminate()
                kill = None
                return True
            except Exception as e:
                pass
        return False

    def remove(self, filename, maxWait=1, ):
        if (not os.path.exists(filename)):
            return True

        if (maxWait == 0):
            try:
                os.remove(filename) 
                return True
            except Exception as e:
                return False
        else:
            chktime = time.time()
            while (os.path.exists(filename)) and ((time.time() - chktime) <= maxWait):
                try:
                    os.remove(filename)
                    return True
                except Exception as e:
                    pass
                time.sleep(0.10)

            if (not os.path.exists(filename)):
                return True
            else:
                return False

    def copy(self, fromFile, toFile, ):
        try:
            shutil.copy2(fromFile, toFile)
            return True
        except Exception as e:
            return False

    def txtsWrite(self, filename, txts=[''], encoding='utf-8', exclusive=False, mode='w', ):
        if (exclusive == False):
            try:
                w = codecs.open(filename, mode, encoding)
                for txt in txts:
                    if (encoding != 'shift_jis'):
                        w.write(txt + '\n')
                    else:
                        w.write(txt + '\r\n')
                w.close()
                w = None
                return True
            except Exception as e:
                w = None
                return False
        else:
            res = self.remove(filename, )
            if (res == False):
                return False
            else:
                f2 = filename[:-4] + '.tmp.txt'
                res = self.remove(f2, )
                if (res == False):
                    return False
                else:
                    try:
                        w = codecs.open(f2, mode, encoding)
                        for txt in txts:
                            if (encoding != 'shift_jis'):
                                w.write(txt + '\n')
                            else:
                                w.write(txt + '\r\n')
                        w.close()
                        w = None
                        os.rename(f2, filename)
                        return True
                    except Exception as e:
                        w = None
                        return False

    def txtsRead(self, filename, encoding='utf-8', exclusive=False, ):
        if (not os.path.exists(filename)):
            return False, ''

        encoding2 = encoding
        if (encoding2 == 'utf-8'):
            encoding2 =  'utf-8-sig'

        if (exclusive == False):
            try:
                txts = []
                txt  = ''
                r = codecs.open(filename, 'r', encoding2)
                for t in r:
                    t = t.replace('\n', '')
                    t = t.replace('\r', '')
                    txt  = (txt + ' ' + str(t)).strip()
                    txts.append(t)
                r.close
                r = None
                return txts, txt
            except Exception as e:
                r = None
                return False, ''
        else:
            f2 = filename[:-4] + '.wrk.txt'
            res = self.remove(f2, )
            if (res == False):
                return False
            else:
                try:
                    os.rename(filename, f2)
                    txts = []
                    txt  = ''
                    r = codecs.open(f2, 'r', encoding2)
                    for t in r:
                        t = t.replace('\n', '')
                        t = t.replace('\r', '')
                        txt = (txt + ' ' + str(t)).strip()
                        txts.append(t)
                    r.close
                    r = None
                    self.remove(f2, )
                    return txts, txt
                except Exception as e:
                    r = None
                    return False, ''

    def statusSet(self, filename='', Flag=True, txt='_on_'):
        if (Flag == True):
            chktime = time.time()
            while (not os.path.exists(filename)) and ((time.time() - chktime) < 1):
                try:
                    w = open(filename, 'w')
                    w.write(txt)
                    w.close()
                    w = None
                    return True
                except Exception as e:
                    w = None
                time.sleep(0.10)
        else:
            chktime = time.time()
            while (os.path.exists(filename)) and ((time.time() - chktime) < 1):
                try:
                    os.remove(filename, )
                    return True
                except Exception as e:
                    pass
                time.sleep(0.10)
        return False

    def statusCheck(self, filename='', ):
        if (os.path.exists(filename)):
            return True
        else:
            return False

    def statusWait_false(self, filename, falseWait=1, ):
        if (falseWait != 0):
            chktime = time.time()
            while (os.path.exists(filename)) and ((time.time() - chktime) < falseWait):
                time.sleep(0.10)
        return self.statusCheck(filename)

    def txtFilePath(self, txt='',):
        if (txt == ''):
            return False
        chk = txt.replace('\\','/')
        if (os.path.isfile(chk)) \
        or (os.path.isdir(chk)):
            return chk
        return False

    def txt2filetxt(self, txt='', ):
        ftxt = txt.replace(' ','_')
        ftxt = ftxt.replace(u'　','_')
        ftxt = ftxt.replace(u'、','_')
        ftxt = ftxt.replace(u'。','_')
        ftxt = ftxt.replace('"','_')
        ftxt = ftxt.replace('$','_')
        ftxt = ftxt.replace('%','_')
        ftxt = ftxt.replace('&','_')
        ftxt = ftxt.replace("'",'_')
        ftxt = ftxt.replace('\\','_')
        ftxt = ftxt.replace('|','_')
        ftxt = ftxt.replace('*','_')
        ftxt = ftxt.replace('/','_')
        ftxt = ftxt.replace('?','_')
        ftxt = ftxt.replace(':',',')
        ftxt = ftxt.replace('<','_')
        ftxt = ftxt.replace('>','_')
        return ftxt

    def url2filepath(self, txt='', ):
        # EDGE
        s = txt.find('プロファイル 1 - Microsoft')
        if (s >= 0):
            txt = txt[:s] + 'MicrosoftEdge'

        # 前後逆転
        s = txt.find(' - ')
        if (s < 0):
            ftxt = txt
        else:
            ftxt = txt[s+2:] + '/' + txt[:s]

        # HTTP
        ftxt = ftxt.replace('https://','')
        ftxt = ftxt.replace('http://','')
        ftxt = ftxt.replace('//','/')
        ftxt = ftxt.replace('/#','/')
        s = ftxt.find('?')
        if (s >= 0):
            ftxt = ftxt[:s]
        s = ftxt.find('#')
        if (s >= 0):
            ftxt = ftxt[:s]

        ftxt = ftxt.replace(u' ','')
        ftxt = ftxt.replace(u'　','_')
        ftxt = ftxt.replace(u'、','.')
        ftxt = ftxt.replace(u'。','.')
        ftxt = ftxt.replace('"','')
        ftxt = ftxt.replace('$','_')
        ftxt = ftxt.replace('%','_')
        ftxt = ftxt.replace('&','_')
        ftxt = ftxt.replace("'",'')
        ftxt = ftxt.replace('\\','_')
        ftxt = ftxt.replace('|','_')
        ftxt = ftxt.replace('*','_')
        ftxt = ftxt.replace('?','_')
        ftxt = ftxt.replace(':',',')
        ftxt = ftxt.replace('<','_')
        ftxt = ftxt.replace('>','_')
        ftxt = ftxt.replace('(','')
        ftxt = ftxt.replace(')','')
        ftxt = ftxt.replace('.','_')
        return ftxt



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



    def img2clip(self, file):
        if (os.name == 'nt'):
            #try:
                img = Image.open(file)
                output = io.BytesIO()
                img.convert('RGB').save(output, 'BMP')
                data = output.getvalue()[14:]
                output.close()

                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                win32clipboard.CloseClipboard()
                return True
            #except Exception as e:
            #    pass
        return False



    def in_japanese(self, txt=''):
        t = txt.replace('\r', '')
        t = t.replace('\n', '')
        try:
            for s in t:
                name = unicodedata.name(s) 
                if ('CJK UNIFIED' in name) \
                or ('HIRAGANA' in name) \
                or ('KATAKANA' in name):
                    return True
        except Exception as e:
            pass
        return False



    def waitSec(self, sec=0, ):
        xSec = sec
        while (int(xSec) > 0):
            print('wait … ' + str(int(xSec)))
            time.sleep(1)
            xSec -= 1
        if (xSec > 0):
            time.sleep(xSec)
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

    def notePad(self, txt='', cr=True, lf=False, ):
        winTitle  = u'無題 - メモ帳'
        if (os.name != 'nt'):
            return False

        parent_handle = ctypes.windll.user32.FindWindowW(0, winTitle)
        if (parent_handle == 0):
            return False
        else:
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

    def guideSound(self, filename=None, sync=True):
        playfile = filename
        if (filename == '_up'):
            playfile = qPath_sounds + '_sound_up.mp3'
        if (filename == '_ready'):
            playfile = qPath_sounds + '_sound_ready.mp3'
        if (filename == '_accept'):
            playfile = qPath_sounds + '_sound_accept.mp3'
        if (filename == '_ok'):
            playfile = qPath_sounds + '_sound_ok.mp3'
        if (filename == '_ng'):
            playfile = qPath_sounds + '_sound_ng.mp3'
        if (filename == '_down'):
            playfile = qPath_sounds + '_sound_down.mp3'
        if (filename == '_shutter'):
            playfile = qPath_sounds + '_sound_shutter.mp3'
        if (filename == '_pingpong'):
            playfile = qPath_sounds + '_sound_pingpong.mp3'

        if (os.path.exists(playfile)):

            sox=subprocess.Popen(['sox', '-q', playfile, '-d', ], \
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            if (sync == True):
                sox.wait()
                sox.terminate()
                sox = None

            return True

        return False

    def chkSelfDev(self, dev=None, ):
        if (dev is None):
            return False
        elif (dev.isdigit()):
            return True
        elif (str(dev).lower().find('localhost')  >= 0):
            return True
        elif (str(dev).lower().find(qHOSTNAME) >= 0):
            return True
        else:
            return False

    # qFunc,qGuide 共通
    def cv2pil(self, cv2_image=None):
        try:
            wrk_image = cv2_image.copy()
            if (wrk_image.ndim == 2):  # モノクロ
                pass
            elif (wrk_image.shape[2] == 3):  # カラー
                wrk_image = cv2.cvtColor(wrk_image, cv2.COLOR_BGR2RGB)
            elif (wrk_image.shape[2] == 4):  # 透過
                wrk_image = cv2.cvtColor(wrk_image, cv2.COLOR_BGRA2RGBA)
            pil_image = Image.fromarray(wrk_image)
            return pil_image
        except:
            pass
        return None

    # qFunc,qGuide 共通
    def pil2cv(self, pil_image=None):
        try:
            cv2_image = np.array(pil_image, dtype=np.uint8)
            if (cv2_image.ndim == 2):  # モノクロ
                pass
            elif (cv2_image.shape[2] == 3):  # カラー
                cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)
            elif (cv2_image.shape[2] == 4):  # 透過
                cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGBA2BGRA)
            return cv2_image
        except:
            pass
        return None

    # qFunc,qGuide 共通
    def getPanelPos(self, id='0-', ):
        #left, top, width, height = getPanelPos(panel,)

        w, h = pyautogui.size()
        wa = int(w/100) 
        ha = int(h/100) 
        wb = int(w/20) 
        hb = int(h/20) 
        if   (id == '0'):
            return 0, 0, w, h
        elif (id == '0-'):
            return wb, hb, int(w-wb*2), int(h-hb*2)
        elif (id == '0+'):
            return -30, -30, w+60, h+60
        elif (id == '1'):
            return 0, 0, int(w/3), int(h/3)
        elif (id == '1-'):
            return 0+wa, 0+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (id == '2'):
            return int(w/3), 0, int(w/3), int(h/3)
        elif (id == '2-'):
            return int(w/3)+wa, 0+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (id == '3'):
            return w-int(w/3), 0, int(w/3), int(h/3)
        elif (id == '3-'):
            return w-int(w/3)+wa, 0+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (id == '4'):
            return 0, int(h/3), int(w/3), int(h/3)
        elif (id == '4-'):
            return 0+wa, int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (id == '5'):
            return int(w/3), int(h/3), int(w/3), int(h/3)
        elif (id == '5-'):
            return int(w/3)+wa, int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (id == '5+'):
            return int(w/4), int(h/4), int(w/2), int(h/2)
        elif (id == '6'):
            return w-int(w/3), int(h/3), int(w/3), int(h/3)
        elif (id == '6-'):
            return w-int(w/3)+wa, int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (id == '7'):
            return 0, h-int(h/3), int(w/3), int(h/3)
        elif (id == '7-'):
            return 0+wa, h-int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (id == '8'):
            return int(w/3), h-int(h/3), int(w/3), int(h/3)
        elif (id == '8-'):
            return int(w/3)+wa, h-int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        elif (id == '9'):
            return w-int(w/3), h-int(h/3), int(w/3), int(h/3)
        elif (id == '9-'):
            return w-int(w/3)+wa, h-int(h/3)+ha, int((w/3)-wa*2), int((h/3)-ha*2)
        else:
            return int(w/4), int(h/4), int(w/2), int(h/2)

    def getResolution(self, reso='full', ):
        if (reso == 'full')  \
        or (reso == 'full+') \
        or (reso == 'full-'):
            if (self.qScreenWidth == 0):
                try:
                    self.qScreenWidth, self.qScreenHeight = pyautogui.size()
                except Exception as e:
                    self.qScreenHeight =  720
                    self.qScreenWidth  = 1280

        if   (reso == 'full'): 
            return self.qScreenWidth, self.qScreenHeight
        if   (reso == 'full+'):
            return self.qScreenWidth + 90, self.qScreenHeight + 50
        if   (reso == 'full-'):
            return int(self.qScreenWidth*0.9), int(self.qScreenHeight*0.9)
        elif (reso == 'half'):
            return int(self.qScreenWidth/2), int(self.qScreenHeight/2)

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



class qFPS_class(object):
    def __init__(self):
        self.start     = cv2.getTickCount()
        self.count     = 0
        self.FPS       = 0
        self.lastcheck = time.time()
    def get(self):
        self.count += 1
        if (self.count >= 15) or ((time.time() - self.lastcheck) > 5):
            nowTick  = cv2.getTickCount()
            diffSec  = (nowTick - self.start) / cv2.getTickFrequency()
            self.FPS = 1 / (diffSec / self.count)
            self.start = cv2.getTickCount()
            self.count = 0
            self.lastcheck = time.time()
        return self.FPS



if (__name__ == '__main__'):

    qFunc = qFunc_class()
    qFunc.init()

    qFunc.kill('sox')

    qFunc.notePad(txt=u'開始')
    #qFunc.sendKey(txt=u'日本語')
    #qFunc.sendKey(txt=u'abcdefg',lf=False)

    x,y = qFunc.getResolution('full')
    print('getResolution x,y = ', x, y, )

    qFunc.img2clip('cv2dnn\dog.jpg')

    qFunc.notePad(txt=u'終了')

    print(qFunc.chkSelfDev('http://localhost:...'))



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
