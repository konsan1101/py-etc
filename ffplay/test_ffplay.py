#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import time
import threading
import os

import pyautogui
if (os.name == 'nt'):
    import ctypes

def ffplay(id='ffplay', file='', vol=100, order=-1, left=0, top=0, width=640, height=480,):

    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -x 320 -y 240
    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -fs

    if (width != 0) or (height != 0):
        ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                    '-volume', str(vol), \
                                    '-window_title', str(id), \
                                    '-noborder', '-autoexit', \
                                    '-x', str(width), '-y', str(height), \
                                    '-loglevel', 'warning', \
                    ], )
                    #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    else:
        w, h = pyautogui.size()
        ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                    '-volume', str(vol), \
                                    '-window_title', str(id), \
                                    '-noborder', '-autoexit', \
                                    #'-fs', \
                                    '-x', str(w), '-y', str(h), \
                                    '-loglevel', 'warning', \
                    ], )
                    #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

    z_order = 0
    if (order == 'top'):
        z_order = -1

    if (os.name == 'nt'):
        hwnd = 0
        chktime = time.time()
        while (hwnd == 0) and ((time.time() - chktime) < 3):
            hwnd = ctypes.windll.user32.FindWindowW(None, str(id))
            time.sleep(0.10)

    if (width != 0) or (height != 0):
        if (os.name == 'nt'):
            if (hwnd != 0):
                ctypes.windll.user32.SetWindowPos(hwnd,z_order,int(left),int(top),0,0,1)
    else:
        if (os.name == 'nt'):
            if (hwnd != 0):
                ctypes.windll.user32.SetWindowPos(hwnd,z_order,0,0,0,0,1)

    ffplay.wait()
    ffplay.terminate()
    ffplay = None



if __name__ == '__main__':

    id = 'Player 0'
    file = "test_input.flv"
    play0 = threading.Thread(target=ffplay, args=(id, file, 0, 'normal', 0, 0, 0, 0, ), )
    play0.setDaemon(True)
    play0.start()

    time.sleep(3)

    id = 'Player 1'
    file = "test_input.flv"
    play1 = threading.Thread(target=ffplay, args=(id, file, 100, 'top', 100, 100, 320, 240, ), )
    play1.setDaemon(True)
    play1.start()

    time.sleep(3)

    id = 'Player 2'
    file = "test_input.flv"
    play2 = threading.Thread(target=ffplay, args=(id, file, 100, 'normal', 300, 300, 320, 240, ), )
    play2.setDaemon(True)
    play2.start()

    time.sleep(3)

    while (play1.is_alive()):
        print('play1_alive')
        time.sleep(1)

    play0.join()
    del play0
    play1.join()
    del play1
    play2.join()
    del play2


