#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import numpy as np
import cv2

import pyautogui
import subprocess



def fullCapture(full=True, workpath='temp/_work/caputure.', ):
    capture = None

    # フルキャプチャ
    if (full == True) and (os.name == 'nt'):
        # ファイル削除
        for i in range(1, 9):
            fn = workpath + '{:04}'.format(i) + '.jpg'
            if os.path.isfile(fn):
                os.remove(fn)
            else:
                break
        # キャプチャー
        ffmpeg = subprocess.Popen(['ffmpeg', '-f', 'gdigrab', '-i', 'desktop',
                                '-ss','0','-t','0.2','-r','10','-qmin','1','-q','1', workpath + '%04d.jpg',
                                '-loglevel', 'warning',],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        # 時限待機・終了
        checkTime = time.time()
        while ((time.time() - checkTime) < 2):
            # バッファから1行読み込む.
            line = ffmpeg.stderr.readline()
            # バッファが空 + プロセス終了.
            if (not line) and (not ffmpeg.poll() is None):
                break
        ffmpeg.terminate()
        ffmpeg = None
        # イメージ取得
        try:
            capture = cv2.imread(workpath + '0001.jpg')
        except:
            capture = None

        # メインキャプチャ
        if (capture is None):
            pil_image = pyautogui.screenshot()
            capture = np.array(pil_image, dtype=np.uint8)
            if (capture.ndim == 2):  # モノクロ
                pass
            elif (capture.shape[2] == 3):  # カラー
                capture = cv2.cvtColor(capture, cv2.COLOR_RGB2BGR)
            elif (capture.shape[2] == 4):  # 透過
                capture = cv2.cvtColor(capture, cv2.COLOR_RGBA2BGRA)

    return capture



if __name__ == '__main__':

    img = fullCapture(workpath='./')
    cv2.imshow("", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


