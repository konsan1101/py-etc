#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2020 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import os
import time

import queue
import threading
import subprocess

import pyautogui
import numpy as np
import cv2



class qFFmpeg_class:

    def __init__(self, ): 
        self.face_procWidth  = 640
        self.face_procHeight = 480
        self.face_casName    = '_xml/_vision_opencv_face.xml'
        self.face_cascade    = cv2.CascadeClassifier(self.face_casName)
        self.face_haar_scale    = 1.1
        self.face_min_neighbors = 10
        self.face_min_size      = ( 15, 15)

    def detect_face(self, inp_image=None, ):
        output_img  = inp_image
        output_face = []

        try:

                image_img   = inp_image.copy()
                image_height, image_width = image_img.shape[:2]

                output_img  = image_img.copy()

                proc_width  = image_width
                proc_height = image_height
                if (proc_width  > self.face_procWidth):
                    proc_width  = self.face_procWidth
                    proc_height = int(proc_width * image_height / image_width)
                if (proc_width  != image_width ) \
                or (proc_height != image_height):
                    proc_img = cv2.resize(image_img, (proc_width, proc_height))
                else:
                    proc_img = image_img.copy()
                    proc_height, proc_width = proc_img.shape[:2]

                gray1 = cv2.cvtColor(proc_img, cv2.COLOR_BGR2GRAY)
                gray2 = cv2.equalizeHist(gray1)

                hit_count = 0
                hit_img   = None

                rects = self.face_cascade.detectMultiScale(gray2, 
                        scaleFactor=self.face_haar_scale,
                        minNeighbors=self.face_min_neighbors,
                        minSize=self.face_min_size, )
                if (not rects is None):
                    for (hit_x, hit_y, hit_w, hit_h) in rects:
                        hit_count += 1
                        x  = int(hit_x * image_width  / proc_width )
                        y  = int(hit_y * image_height / proc_height)
                        w  = int(hit_w * image_width  / proc_width )
                        h  = int(hit_h * image_height / proc_height)
                        if (x > 10):
                            x -= 10
                            w += 20
                        if (y > 10):
                            y -= 10
                            h += 20
                        if (x < 0):
                            x = 0
                        if (y < 0):
                            y = 0
                        if ((x + w) > image_width):
                                w = image_width - x
                        if ((y + h) > image_height):
                                h = image_height - y
                        cv2.rectangle(output_img, (x,y), (x+w,y+h), (0,0,255), 2)

                        hit_img = cv2.resize(image_img[y:y+h, x:x+w],(h,w))

                        # 結果出力
                        output_face.append(hit_img)

        except:
            pass

        return output_img, output_face

    def dshow_dev_list(self, ):
        cam = []
        mic = []

        if (os.name == 'nt'):

            ffmpeg = subprocess.Popen(['ffmpeg',
	            '-threads', '2',
	            '-f', 'dshow',
	            '-list_devices', 'true',
	            '-i', 'nul',
	            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            flag = ''
            checkTime = time.time()
            while ((time.time() - checkTime) < 2):
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
                    #print('cam:', txt[st:st+en])
                elif (flag == 'mic') and (txt.find(']  "') >=0):
                    st = txt.find(']  "') + 4
                    en = txt[st:].find('"')
                    mic.append(txt[st:st+en])
                    #print('mic:', txt[st:st+en])

            ffmpeg.terminate()
            ffmpeg = None

        return cam, mic

    def capture(self, dev='desktop', full=True, 
                work_path='temp/_work/desktop', retry_max=1, retry_wait=2.00, ):

        retry_max   = 3
        retry_count = 0
        check       = False
        while (check == False) and (retry_count <= retry_max):
            # キャプチャー
            image = self.capture_sub(dev, full, work_path)
            if (not image is None):
                check = True
            # リトライ
            if (check == False):
                time.sleep(retry_wait)

        if (check == True):
            return image
        else:
            return None

    def capture_sub(self, dev='desktop', full=True, 
                    work_path='temp/_work/desktop', ):
        capture = None

        # ファイル削除
        for i in range(1, 9999):
            fn = work_path + '.' + '{:04}'.format(i) + '.jpg'
            if os.path.isfile(fn):
                os.remove(fn)
            else:
                break

        # pyautogui キャプチャ
        if (capture is None):
            if (dev == 'desktop') and (full == False):

                pil_image = pyautogui.screenshot()
                capture = np.array(pil_image, dtype=np.uint8)
                if (capture.ndim == 2):  # モノクロ
                    pass
                elif (capture.shape[2] == 3):  # カラー
                    capture = cv2.cvtColor(capture, cv2.COLOR_RGB2BGR)
                elif (capture.shape[2] == 4):  # 透過
                    capture = cv2.cvtColor(capture, cv2.COLOR_RGBA2BGRA)

                # イメージ保存
                #try:
                #    cv2.imwrite(workpath + '.0001.jpg', capture)
                #except:
                #    capture = None

        # ffmpag キャプチャ
        if (capture is None):

            ffmpeg = None

            # デスクトップ
            if (dev == 'desktop'):
                if (os.name == 'nt'):

                    ffmpeg = subprocess.Popen(['ffmpeg', 
                        '-threads', '2',
                        '-f', 'gdigrab', '-i', 'desktop',
                        '-ss','0','-t','0.2','-r','10',
                        '-q','1', 
                        work_path + '.' + '%04d.jpg',
                        '-loglevel', 'warning',
                        #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                else:

                    ffmpeg = subprocess.Popen(['ffmpeg', 
                        '-threads', '2',
                        '-f', 'avfoundation', '-i', '1:2',
                        '-ss','0','-t','0.2','-r','10',
                        '-q','1', 
                        work_path + '.' + '%04d.jpg',
                        '-loglevel', 'warning',
                        #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # カメラ
            if (dev != 'desktop'):
                if (os.name == 'nt'):

                    ffmpeg = subprocess.Popen(['ffmpeg', 
                        '-threads', '2',
                        '-rtbufsize', '1024M',
                        '-f', 'dshow', '-i', 'video=' + dev,
                        '-ss','0','-t','0.2','-r','10',
                        '-q','1', 
                        work_path + '.' + '%04d.jpg',
                        '-loglevel', 'warning',
                        #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                        ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # 時限待機・画像取得
            if (not ffmpeg is None):
                checkTime = time.time()
                while ((time.time() - checkTime) < 2):
                    line = ffmpeg.stderr.readline()
                    #print(line)
                    if (not line) and (not ffmpeg.poll() is None):
                        break
                ffmpeg.terminate()
                ffmpeg = None

            # イメージ取得
            try:
                capture = cv2.imread(work_path + '.0001.jpg')
            except:
                capture = None

        return capture

    def rec_start(self, dev='desktop', rate=10, 
                    out_filev='temp/_work/recorder.mp4', out_filea='temp/_work/recorder.wav',
                    retry_max=3, retry_wait=5.00, ):

        #retry_max   = 3
        retry_count = 0
        check       = False
        while (check == False) and (retry_count <= retry_max):
            # 録画
            res_ffmpeg, res_sox, res_filev, res_filea = self.rec_start_sub(
                dev=dev, rate=rate, out_filev=out_filev, out_filea=out_filea, try_count=retry_count, )
            # チェック
            if (not res_ffmpeg is None) or (not res_sox is None):
                check = True
            # リトライ
            if (check == False) and (retry_count < retry_max):
                #print('retry')
                time.sleep(retry_wait)
                retry_count += 1

        if (check == True):
            return res_ffmpeg, res_sox, res_filev, res_filea
        else:
            return None, None, '', ''

    def rec_start_sub(self, dev='desktop', rate=10,
                        out_filev='temp/_work/recorder.mp4', out_filea='temp/_work/recorder.wav',
                        try_count=0, ):
        res_ffmpeg = None
        res_sox    = None
        res_filev  = out_filev
        res_filea  = out_filea

        # 録画　開始
        if (res_filev != ''):

            # デスクトップ Linux
            if (res_ffmpeg == None) and (dev == 'desktop'):
                if (os.name != 'nt'):

                        if (res_filev[-4:] != '.flv'):
                            res_filev = res_filev[:-4] + '.flv'

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # ffmpeg -f avfoundation -i 1:2 -vcodec flv1 -q:v 0 -r 10 desktop.flv
                        res_ffmpeg = subprocess.Popen(['ffmpeg',
                            '-threads', '2',
                            '-f', 'avfoundation',
                            '-i', '1:2',
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'flv1',
                            '-q:v', '0',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                            ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # デスクトップ Windows ※初回
            if (res_ffmpeg == None) and (dev == 'desktop'):
                if (os.name == 'nt'):
                    if (try_count == 0) and (res_filev[-4:] == '.mp4'):

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # GPU encoder, intel GPU 6th enable !
                        # ffmpeg -init_hw_device qsv:hw -f gdigrab -i desktop -vcodec hevc_qsv -r 10 desktop.mp4
                        res_ffmpeg = subprocess.Popen(['ffmpeg',
                            '-threads', '2',
                            '-init_hw_device', 'qsv:hw',
                            '-f', 'gdigrab', '-i', 'desktop',
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'hevc_qsv',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                            ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # デスクトップ Windows ※２回目
            if (res_ffmpeg == None) and (dev == 'desktop'):
                if (os.name == 'nt'):
                    if (try_count == 1) and (res_filev[-4:] == '.mp4'):

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # GPU encoder, intel GPU enable !
                        # ffmpeg -init_hw_device qsv:hw -f gdigrab -i desktop -vcodec h264_qsv -r 10 desktop.mp4
                        res_ffmpeg = subprocess.Popen(['ffmpeg',
                            '-threads', '2',
                            '-init_hw_device', 'qsv:hw',
                            '-f', 'gdigrab', '-i', 'desktop',
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'h264_qsv',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                            ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # デスクトップ Windows ※３回目以降
            if (res_ffmpeg == None) and (dev == 'desktop'):
                if (os.name == 'nt'):
                    if (try_count >= 2):

                        if (res_filev[-4:] != '.flv'):
                            res_filev = res_filev[:-4] + '.flv'

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # ffmpeg -f gdigrab -i desktop -vcodec flv1 -q:v 0 -r 10 desktop.flv
                        res_ffmpeg = subprocess.Popen(['ffmpeg',
                            '-threads', '2',
                            '-f', 'gdigrab', '-i', 'desktop',
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'flv1',
                            '-q:v', '0',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                            ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # カメラ Windows ※初回
            if (res_ffmpeg == None) and (dev != 'desktop'):
                if (os.name == 'nt'):
                    if (try_count == 0) and (res_filev[-4:] == '.mp4'):

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # GPU encoder, intel 6th GPU enable !
                        # ffmpeg -init_hw_device qsv:hw -rtbufsize 1024M -f dshow -i "video=Microsoft Camera Front" -vcodec hevc_qsv -r 10 camera.mp4
                        res_ffmpeg = subprocess.Popen(['ffmpeg',
                            '-threads', '2',
                            '-init_hw_device', 'qsv:hw',
                            '-rtbufsize', '1024M',
                            '-f', 'dshow', '-i', 'video=' + dev,
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'hevc_qsv',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                            ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # カメラ Windows ※２回目
            if (res_ffmpeg == None) and (dev != 'desktop'):
                if (os.name == 'nt'):
                    if (try_count == 1) and (res_filev[-4:] == '.mp4'):

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # GPU encoder, intel GPU enable !
                        # ffmpeg -init_hw_device qsv:hw -rtbufsize 1024M -f dshow -i "video=Microsoft Camera Front" -vcodec h264_qsv -r 10 camera.mp4
                        res_ffmpeg = subprocess.Popen(['ffmpeg',
                            '-threads', '2',
                            '-init_hw_device', 'qsv:hw',
                            '-rtbufsize', '1024M',
                            '-f', 'dshow', '-i', 'video=' + dev,
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'h264_qsv',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                            ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

            # カメラ Windows ※３回目以降
            if (res_ffmpeg == None) and (dev != 'desktop'):
                if (os.name == 'nt'):
                    if (try_count >= 2):

                        if (res_filev[-4:] != '.flv'):
                            res_filev = res_filev[:-4] + '.flv'

                        if (os.path.isfile(res_filev)):
                            os.remove(res_filev)

                        # ffmpeg -rtbufsize 1024M -f dshow -i "video=Microsoft Camera Front" -vcodec flv1 -q:v 0 -r 10 camera.flv
                        res_ffmpeg = subprocess.Popen(['ffmpeg',
                            '-threads', '2',
                            '-rtbufsize', '1024M',
                            '-f', 'dshow', '-i', 'video=' + dev,
                            '-vf', 'scale=1920:-2',
                            '-vcodec', 'flv1',
                            '-q:v', '0',
                            '-r', str(rate),
                            res_filev,
                            '-loglevel', 'warning',
                            #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                            ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        # 録音　開始
        if (res_filea != ''):

            if (os.path.isfile(res_filea)):
                os.remove(res_filea)

            res_sox = subprocess.Popen(['sox',
                '-q', '-d', '-r', '16000', '-b', '16', '-c', '1',
                res_filea,
                #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        # 起動確認
        time.sleep(5.00)

        check = True
        if (res_filev != ''):
            if (not os.path.isfile(res_filev)):
                check = False
            else:
                if (os.path.getsize(res_filev) == 0):
                    check = False
        #if (res_filea != ''):
        #    if (not os.path.isfile(res_filea)):
        #        check = False
        #    else:
        #        if (os.path.getsize(res_filea) == 0):
        #            check = False

        # 起動エラー
        if (check == False):
            if (res_filev != ''):
                if (not res_ffmpeg is None):
                    res_ffmpeg.terminate()
                    res_ffmpeg = None
                    res_filev  = ''
            if (res_filea != ''):
                if (not res_sox is None):
                    res_sox.terminate()
                    res_sox    = None
                    res_filea  = ''

        return res_ffmpeg, res_sox, res_filev, res_filea

    def rec_stop(self, ffmpeg, sox, ):

        # 録画　停止
        if (not ffmpeg is None):
            ffmpeg.stdin.write(b'q\n')
            try:
                ffmpeg.stdin.flush()
            except Exception as e:
                pass

        # 録音　停止・終了
        if (not sox is None):
            #if (os.name != 'nt'):
            #    sox.send_signal(signal.SIGINT)
            #else:
            #    sox.send_signal(signal.CTRL_C_EVENT)
            #time.sleep(2.00)
            sox.terminate()
            sox = None

        # 録画　時限待機・終了
        if (not ffmpeg is None):
            checkTime = time.time()
            while ((time.time() - checkTime) < 5):
                line = ffmpeg.stderr.readline()
                if (not line) and (not ffmpeg.poll() is None):
                    break

            #logb, errb = ffmpeg.communicate()
            ffmpeg.wait()
            ffmpeg.terminate()
            ffmpeg = None

        return True

    def encodemp4mp3(self, inp_filev='temp/_work/recorder.mp4', inp_filea='temp/_work/recorder.wav', rate=10,
                    out_filev='temp/_work/recorder_h265.mp4', out_filea='temp/_work/recorder_mp3.mp3', ):

        mp4ok = False
        mp3ok = False

        # 音声確認
        if (inp_filea != ''):
            if (not os.path.isfile(inp_filea)):
                inp_filea = ''
                out_filea = ''
            else:
                if (os.path.getsize(inp_filea) <= 44):
                    inp_filea = ''
                    out_filea = ''

        # 動画＋音声変換

        # GPU encoder 変換
        if (mp4ok == False) and (os.name == 'nt'):
            if (inp_filev != '') and (inp_filea != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # GPU encoder, intel 6th GPU enable !
                ffmpeg = subprocess.Popen(['ffmpeg',
                    '-threads', '2',
                    '-init_hw_device', 'qsv:hw',
                    '-i', inp_filev, '-i', inp_filea,
                    '-vf', 'scale=1920:-1',
                    '-vcodec', 'hevc_qsv', '-r', str(rate),
                    '-acodec', 'libmp3lame', '-strict', 'unofficial', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    #'-acodec', 'aac', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    out_filev,
                    '-loglevel', 'warning',
                    #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # GPU encoder 変換
        if (mp4ok == False) and (os.name == 'nt'):
            if (inp_filev != '') and (inp_filea != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # GPU encoder, intel GPU enable !
                ffmpeg = subprocess.Popen(['ffmpeg',
                    '-threads', '2',
                    '-init_hw_device', 'qsv:hw',
                    '-i', inp_filev, '-i', inp_filea,
                    '-vf', 'scale=1920:-1',
                    '-vcodec', 'h264_qsv', '-r', str(rate),
                    '-acodec', 'libmp3lame', '-strict', 'unofficial', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    #'-acodec', 'aac', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    out_filev,
                    '-loglevel', 'warning',
                    #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # software encoder 変換
        if (mp4ok == False):
            if (inp_filev != '') and (inp_filea != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # software encoder,
                ffmpeg = subprocess.Popen(['ffmpeg',
                    '-threads', '2',
                    '-i', inp_filev, '-i', inp_filea,
                    '-vcodec', 'libx265', '-r', str(rate),
                    '-acodec', 'libmp3lame', '-strict', 'unofficial', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    #'-acodec', 'aac', '-ab', '96k', '-ac', '1', '-ar', '16000',
                    out_filev,
                    '-loglevel', 'warning',
                    #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # 動画変換

        # GPU encoder 変換
        if (mp4ok == False) and (os.name == 'nt'):
            if (inp_filev != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # GPU encoder, intel 6th GPU enable !
                ffmpeg = subprocess.Popen(['ffmpeg',
                    '-threads', '2',
                    '-init_hw_device', 'qsv:hw',
                    '-i', inp_filev,
                    '-vf', 'scale=1920:-1',
                    '-vcodec', 'hevc_qsv', '-r', str(rate),
                    out_filev,
                    '-loglevel', 'warning',
                    #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # GPU encoder 変換
        if (mp4ok == False) and (os.name == 'nt'):
            if (inp_filev != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # GPU encoder, intel GPU enable !
                ffmpeg = subprocess.Popen(['ffmpeg',
                    '-threads', '2',
                    '-init_hw_device', 'qsv:hw',
                    '-i', inp_filev,
                    '-vf', 'scale=1920:-1',
                    '-vcodec', 'h264_qsv', '-r', str(rate),
                    out_filev,
                    '-loglevel', 'warning',
                    #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # software encoder 変換
        if (mp4ok == False):
            if (inp_filev != '') and (out_filev != ''):

                if (os.path.isfile(out_filev)):
                    os.remove(out_filev)

                # software encoder,
                ffmpeg = subprocess.Popen(['ffmpeg',
                    '-threads', '2',
                    '-i', inp_filev,
                    '-vcodec', 'libx265', '-r', str(rate),
                    out_filev,
                    '-loglevel', 'warning',
                    #], stdin=subprocess.PIPE, stderr=subprocess.PIPE,)
                    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                #logb, errb = ffmpeg.communicate()
                ffmpeg.wait()
                ffmpeg.terminate()
                ffmpeg = None
                if (os.path.isfile(out_filev)):
                    if (os.path.getsize(out_filev) > 0):
                        mp4ok = True

        # 音声処理
        mp3ok = False
        if (inp_filea != '') and (out_filea != ''):
            sox = subprocess.Popen(['sox', '-q', inp_filea, out_filea,
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
            sox.wait()
            sox.terminate()
            sox = None
            if (os.path.isfile(out_filea)):
                if (os.path.getsize(out_filea) > 0):
                    mp3ok = True

        # 戻り値
        if   (mp4ok == True) and (mp3ok == True):
            return [out_filev, out_filea]
        elif (mp4ok == True) and (mp3ok == False):
            return [out_filev]
        elif (mp4ok == False) and (mp3ok == True):
            return [out_filea]
        else:
            return False



if __name__ == '__main__':

    qPath_work = 'temp/_work'
    if (not os.path.isdir('temp')):
        os.mkdir('temp')
    if (not os.path.isdir('temp/_work')):
        os.mkdir('temp/_work')

    # ffmpeg 操作
    qFFmpeg = qFFmpeg_class()

    # デバイス名取得
    cam, mic = qFFmpeg.dshow_dev_list()

    print('snapshot test')

    # デスクトップ
    print('desktop')

    work_path = qPath_work + 'capture'
    img       = qFFmpeg.capture(dev='desktop', full=True, work_path=work_path, )
    if (not img is None):
        proc_img = cv2.resize(img, (320, 240))
        cv2.imshow('', proc_img)
        cv2.waitKey(1)
        time.sleep(2.00)

    # カメラ
    print('camera')

    count = 0
    for cam_dev in cam:
        count += 1
        work_path = qPath_work + 'capture' + str(count)
        img       = qFFmpeg.capture(dev=cam_dev, full=True, work_path=work_path, )
        if (not img is None):
            out_image, _ = qFFmpeg.detect_face(inp_image=img, )
            if (not out_image is None):
                proc_img = cv2.resize(out_image, (320, 240))
                cv2.imshow('', proc_img)
                cv2.waitKey(1)
                time.sleep(2.00)

    time.sleep(5.00)
    cv2.destroyAllWindows()

    print('recorder test')

    # デスクトップ
    print('start')

    rec_filev = 'temp/_work/recorder.mp4'
    rec_filea = 'temp/_work/recorder.wav'
    ffmpeg, sox, rec_filev, rec_filea = qFFmpeg.rec_start(dev='desktop', rate=10, 
                                                            out_filev=rec_filev, out_filea=rec_filea,
                                                            retry_max=3, retry_wait=5.00,)
    time.sleep(5.00)

    print('stop')

    qFFmpeg.rec_stop(ffmpeg, sox,)
    ffmpeg = None
    sox    = None

    # 動画変換
    print('convert')

    mp4_filev = 'temp/_work/recorder_mp4.mp4'
    mp3_filea = 'temp/_work/recorder_mp3.mp3'
    res = qFFmpeg.encodemp4mp3(inp_filev=rec_filev, inp_filea=rec_filea, rate=10, 
                                out_filev=mp4_filev, out_filea=mp3_filea,)




