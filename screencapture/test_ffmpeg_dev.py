#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import time

def dshow_dev():
    cam = []
    mic = []

    ffmpeg = subprocess.Popen(['ffmpeg', '-f', 'dshow', '-list_devices', 'true', '-i', 'dummy', ],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

    flag = ''
    while True:
        # バッファから1行読み込む.
        line = ffmpeg.stderr.readline()
        # バッファが空 + プロセス終了.
        if (not line) and (not ffmpeg.poll() is None):
            break
        # テキスト
        txt = line.decode('utf-8')
        if   (txt.find('DirectShow video devices') >=0):
            flag = 'cam'
        elif (txt.find('DirectShow audio devices') >=0):
            flag = 'mic'
        elif (flag == 'cam') and (txt.find(']  "') >=0):
            st = txt.find(']  "') + 4
            en = txt[st:].find('"')
            cam.append(txt[st:st+en])
            print('cam:', txt[st:st+en])
        elif (flag == 'mic') and (txt.find(']  "') >=0):
            st = txt.find(']  "') + 4
            en = txt[st:].find('"')
            mic.append(txt[st:st+en])
            print('mic:', txt[st:st+en])

    ffmpeg.terminate()
    ffmpeg = None

    return cam, mic


if __name__ == '__main__':

    cam, mic = dshow_dev()


