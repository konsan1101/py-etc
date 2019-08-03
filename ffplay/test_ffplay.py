#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import ctypes
import time
import threading

def ffplay(file, vol=100, left=0, top=0, width=640, height=480,):

    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -x 320 -y 240
    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -fs

    if (width != 0) or (height != 0):
        ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                    '-volume', str(vol), \
                                    '-window_title', file, \
                                    '-noborder', '-autoexit', \
                                    '-x', '320', '-y', '240', \
                    ], )
                    #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    else:
        ffplay = subprocess.Popen(['ffplay', '-i', file, \
                                    '-volume', str(vol), \
                                    '-window_title', file, \
                                    '-noborder', '-autoexit', \
                                    '-fs', \
                    ], )
                    #], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

    if (width != 0) or (height != 0):
        hwnd = 0
        chktime = time.time()
        while (hwnd == 0) and ((time.time() - chktime) < 3):
            hwnd = ctypes.windll.user32.FindWindowW(None, file)
            time.sleep(0.10)
        if (hwnd != 0):
            ctypes.windll.user32.SetWindowPos(hwnd,-1,100,100,0,0,1)

    ffplay.wait()
    ffplay.terminate()
    ffplay = None



if __name__ == '__main__':

    file = "test_input.flv"
    play1 = threading.Thread(target=ffplay, args=(file, 100, 100, 100, 320, 240, ), )
    play1.setDaemon(True)
    play1.start()

    time.sleep(3)

    play2 = threading.Thread(target=ffplay, args=(file, 100, 300, 300, 320, 240, ), )
    play2.setDaemon(True)
    play2.start()

    time.sleep(3)

    play1.join()
    del play1
    play2.join()
    del play2


