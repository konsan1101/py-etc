#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2020 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import sys
import os
import time
import datetime
import codecs
import glob

import queue
import threading
import subprocess

import numpy as np
import cv2



# 共通ルーチン
import  _v5__qRiKi
qRiKi = _v5__qRiKi.qRiKi_class()
import  _v5__qFunc
qFunc = _v5__qFunc.qFunc_class()
import  _v5__qLog
qLog  = _v5__qLog.qLog_class()
import  _v5__qFFmpeg
qFFmpeg=_v5__qFFmpeg.qFFmpeg_class()

qPLATFORM        = qRiKi.getValue('qPLATFORM'        )
qRUNATTR         = qRiKi.getValue('qRUNATTR'         )
qHOSTNAME        = qRiKi.getValue('qHOSTNAME'        )
qUSERNAME        = qRiKi.getValue('qUSERNAME'        )
qPath_pictures   = qRiKi.getValue('qPath_pictures'   )
qPath_videos     = qRiKi.getValue('qPath_videos'     )
qPath_cache      = qRiKi.getValue('qPath_cache'      )
qPath_sounds     = qRiKi.getValue('qPath_sounds'     )
qPath_icons      = qRiKi.getValue('qPath_icons'      )
qPath_fonts      = qRiKi.getValue('qPath_fonts'      )
qPath_log        = qRiKi.getValue('qPath_log'        )
qPath_work       = qRiKi.getValue('qPath_work'       )
qPath_rec        = qRiKi.getValue('qPath_rec'        )

qPath_s_ctrl     = qRiKi.getValue('qPath_s_ctrl'     )
qPath_s_inp      = qRiKi.getValue('qPath_s_inp'      )
qPath_s_wav      = qRiKi.getValue('qPath_s_wav'      )
qPath_s_jul      = qRiKi.getValue('qPath_s_jul'      )
qPath_s_STT      = qRiKi.getValue('qPath_s_STT'      )
qPath_s_TTS      = qRiKi.getValue('qPath_s_TTS'      )
qPath_s_TRA      = qRiKi.getValue('qPath_s_TRA'      )
qPath_s_play     = qRiKi.getValue('qPath_s_play'     )
qPath_v_ctrl     = qRiKi.getValue('qPath_v_ctrl'     )
qPath_v_inp      = qRiKi.getValue('qPath_v_inp'      )
qPath_v_jpg      = qRiKi.getValue('qPath_v_jpg'      )
qPath_v_detect   = qRiKi.getValue('qPath_v_detect'   )
qPath_v_cv       = qRiKi.getValue('qPath_v_cv'       )
qPath_v_photo    = qRiKi.getValue('qPath_v_photo'    )
qPath_v_msg      = qRiKi.getValue('qPath_v_msg'      )
qPath_d_ctrl     = qRiKi.getValue('qPath_d_ctrl'     )
qPath_d_play     = qRiKi.getValue('qPath_d_play'     )
qPath_d_prtscn   = qRiKi.getValue('qPath_d_prtscn'   )
qPath_d_movie    = qRiKi.getValue('qPath_d_movie'    )
qPath_d_upload   = qRiKi.getValue('qPath_d_upload'   )

qBusy_dev_cpu    = qRiKi.getValue('qBusy_dev_cpu'    )
qBusy_dev_com    = qRiKi.getValue('qBusy_dev_com'    )
qBusy_dev_mic    = qRiKi.getValue('qBusy_dev_mic'    )
qBusy_dev_spk    = qRiKi.getValue('qBusy_dev_spk'    )
qBusy_dev_cam    = qRiKi.getValue('qBusy_dev_cam'    )
qBusy_dev_dsp    = qRiKi.getValue('qBusy_dev_dsp'    )
qBusy_dev_scn    = qRiKi.getValue('qBusy_dev_scn'    )
qBusy_s_ctrl     = qRiKi.getValue('qBusy_s_ctrl'     )
qBusy_s_inp      = qRiKi.getValue('qBusy_s_inp'      )
qBusy_s_wav      = qRiKi.getValue('qBusy_s_wav'      )
qBusy_s_STT      = qRiKi.getValue('qBusy_s_STT'      )
qBusy_s_TTS      = qRiKi.getValue('qBusy_s_TTS'      )
qBusy_s_TRA      = qRiKi.getValue('qBusy_s_TRA'      )
qBusy_s_play     = qRiKi.getValue('qBusy_s_play'     )
qBusy_v_ctrl     = qRiKi.getValue('qBusy_v_ctrl'     )
qBusy_v_inp      = qRiKi.getValue('qBusy_v_inp'      )
qBusy_v_QR       = qRiKi.getValue('qBusy_v_QR'       )
qBusy_v_jpg      = qRiKi.getValue('qBusy_v_jpg'      )
qBusy_v_CV       = qRiKi.getValue('qBusy_v_CV'       )
qBusy_d_ctrl     = qRiKi.getValue('qBusy_d_ctrl'     )
qBusy_d_inp      = qRiKi.getValue('qBusy_d_inp'      )
qBusy_d_QR       = qRiKi.getValue('qBusy_d_QR'       )
qBusy_d_rec      = qRiKi.getValue('qBusy_d_rec'      )
qBusy_d_telework = qRiKi.getValue('qBusy_d_telework' )
qBusy_d_play     = qRiKi.getValue('qBusy_d_play'     )
qBusy_d_browser  = qRiKi.getValue('qBusy_d_browser'  )
qBusy_d_upload   = qRiKi.getValue('qBusy_d_upload'   )
qRdy__s_force    = qRiKi.getValue('qRdy__s_force'    )
qRdy__s_fproc    = qRiKi.getValue('qRdy__s_fproc'    )
qRdy__s_sendkey  = qRiKi.getValue('qRdy__s_sendkey'  )
qRdy__v_mirror   = qRiKi.getValue('qRdy__v_mirror'   )
qRdy__v_reader   = qRiKi.getValue('qRdy__v_reader'   )
qRdy__v_sendkey  = qRiKi.getValue('qRdy__v_sendkey'  )
qRdy__d_reader   = qRiKi.getValue('qRdy__d_reader'   )
qRdy__d_sendkey  = qRiKi.getValue('qRdy__d_sendkey'  )



class proc_capture:

    def __init__(self, name='thread', id='0', runMode='debug', 
        capStretch='0', capRotate='0', capZoom='1.0', capFps='2', ):

        self.runMode    = runMode
        self.capStretch = capStretch
        self.capRotate  = capRotate
        self.capZoom    = capZoom
        self.capFps     = '5'
        if (capFps.isdigit()):
            self.capFps = str(capFps)

        self.breakFlag = threading.Event()
        self.breakFlag.clear()
        self.name      = name
        self.id        = id
        self.proc_id   = '{0:10s}'.format(name).replace(' ', '_')
        self.proc_id   = self.proc_id[:-2] + '_' + str(id)
        if (runMode == 'debug'):
            self.logDisp = True
        else:
            self.logDisp = False
        qLog.log('info', self.proc_id, 'init', display=self.logDisp, )

        self.proc_s    = None
        self.proc_r    = None
        self.proc_main = None
        self.proc_beat = None
        self.proc_last = None
        self.proc_step = '0'
        self.proc_seq  = 0

        # 変数設定
        self.blue_img = np.zeros((240,320,3), np.uint8)
        cv2.rectangle(self.blue_img,(0,0),(320,240),(255,0,0),-1)
        cv2.putText(self.blue_img, 'No Image !', (40,80), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,255))

    def __del__(self, ):
        qLog.log('info', self.proc_id, 'bye!', display=self.logDisp, )

    def begin(self, ):
        #qLog.log('info', self.proc_id, 'start')

        self.fileRun = qPath_work + self.proc_id + '.run'
        self.fileRdy = qPath_work + self.proc_id + '.rdy'
        self.fileBsy = qPath_work + self.proc_id + '.bsy'
        qFunc.statusSet(self.fileRun, False)
        qFunc.statusSet(self.fileRdy, False)
        qFunc.statusSet(self.fileBsy, False)

        self.proc_s = queue.Queue()
        self.proc_r = queue.Queue()
        self.proc_main = threading.Thread(target=self.main_proc, args=(self.proc_s, self.proc_r, ))
        self.proc_beat = time.time()
        self.proc_last = time.time()
        self.proc_step = '0'
        self.proc_seq  = 0

        self.proc_main.setDaemon(True)
        self.proc_main.start()

    def abort(self, waitMax=5, ):
        qLog.log('info', self.proc_id, 'stop', display=self.logDisp, )

        self.breakFlag.set()
        chktime = time.time()
        while (not self.proc_beat is None) and ((time.time() - chktime) < waitMax):
            time.sleep(0.25)
        chktime = time.time()
        while (os.path.exists(self.fileRun)) and ((time.time() - chktime) < waitMax):
            time.sleep(0.25)

    def put(self, data, ):
        self.proc_s.put(data)
        return True

    def checkGet(self, waitMax=5, ):
        chktime = time.time()
        while (self.proc_r.qsize() == 0) and ((time.time() - chktime) < waitMax):
            time.sleep(0.10)
        data = self.get()
        return data

    def get(self, ):
        if (self.proc_r.qsize() == 0):
            return ['', '']
        data = self.proc_r.get()
        self.proc_r.task_done()
        return data

    def main_proc(self, cn_r, cn_s, ):
        # ログ
        qLog.log('info', self.proc_id, 'start', display=self.logDisp, )
        qFunc.statusSet(self.fileRun, True)
        self.proc_beat = time.time()

        # 初期設定
        self.proc_step = '1'

        # ＦＰＳ計測
        qFPS_class = _v5__qFunc.qFPS_class()
        qFPS_last  = time.time()

        # 待機ループ
        self.proc_step = '5'

        while (self.proc_step == '5'):
            self.proc_beat = time.time()

            # 停止要求確認
            if (self.breakFlag.is_set()):
                self.breakFlag.clear()
                self.proc_step = '9'
                break

            # キュー取得
            if (cn_r.qsize() > 0):
                cn_r_get  = cn_r.get()
                inp_name  = cn_r_get[0]
                inp_value = cn_r_get[1]
                cn_r.task_done()
            else:
                inp_name  = ''
                inp_value = ''

            if (cn_r.qsize() > 1) or (cn_s.qsize() > 20):
                qLog.log('warning', self.proc_id, 'queue overflow warning!, ' + str(cn_r.qsize()) + ', ' + str(cn_s.qsize()))

            # レディ設定
            if (qFunc.statusCheck(self.fileRdy) == False):
                qFunc.statusSet(self.fileRdy, True)

            # ステータス応答
            if (inp_name.lower() == '_status_'):
                out_name  = inp_name
                if (not capture is None):
                    out_value = '_ready_'
                else:
                    out_value = '!ready'
                cn_s.put([out_name, out_value])

            # 連携情報
            if (inp_name.lower() == '_capstretch_'):
                self.capStretch = inp_value
                qFPS_last = time.time() - 60
            if (inp_name.lower() == '_caprotate_'):
                self.capRotate = inp_value
                qFPS_last = time.time() - 60
            if (inp_name.lower() == '_capzoom_'):
                self.capZoom = inp_value
                qFPS_last = time.time() - 60



            # 画像処理
            if (cn_s.qsize() == 0):
            #if (True):

                # 画像取得
                work_path = qPath_work + 'capture_' + '{:01}'.format(self.proc_seq % 10)
                frame = qFFmpeg.capture(dev='desktop', full=False, work_path=work_path, )
                #frame = qFFmpeg.capture(dev='desktop', full=True, work_path=work_path, )

                if (not frame is None):

                    # ビジー設定 (ready)
                    if (qFunc.statusCheck(self.fileBsy) == False):
                        qFunc.statusSet(self.fileBsy, True)
                        if (str(self.id) == '0'):
                            qFunc.statusSet(qBusy_d_inp, True)

                    # 実行カウンタ
                    self.proc_last = time.time()
                    self.proc_seq += 1
                    if (self.proc_seq > 9999):
                        self.proc_seq = 1

                    # frame_img
                    frame_img = frame.copy()
                    frame_height, frame_width = frame_img.shape[:2]
                    input_img = frame.copy()
                    input_height, input_width = input_img.shape[:2]

                    # 台形補正
                    if (int(self.capStretch) != 0):
                        x = int((input_width/2) * abs(int(self.capStretch))/100)
                        if (int(self.capStretch) > 0):
                            perspective1 = np.float32([ [x, 0], [input_width-x, 0], [input_width, input_height], [0, input_height] ])
                        else:
                            perspective1 = np.float32([ [0, 0], [input_width, 0], [input_width-x, input_height], [x, input_height] ])
                        perspective2 = np.float32([ [0, 0], [input_width, 0], [input_width, input_height], [0, input_height] ])
                        transform_matrix = cv2.getPerspectiveTransform(perspective1, perspective2)
                        input_img = cv2.warpPerspective(input_img, transform_matrix, (input_width, input_height))

                    # 画像回転
                    if   (int(self.capRotate) == -180):
                        input_img = cv2.flip(input_img, 0) # 180 Rotation Y
                    elif (int(self.capRotate) == -360):
                        input_img = cv2.flip(input_img, 1) # 180 Rotation X
                    elif (abs(int(self.capRotate)) !=   0):
                        width2    = int((input_width - input_height)/2)
                        rect_img  = cv2.resize(input_img[0:input_height, width2:width2+input_height], (960,960))
                        rect_mat  = cv2.getRotationMatrix2D((480, 480), -int(self.capRotate), 1.0)
                        rect_r    = cv2.warpAffine(rect_img, rect_mat, (960, 960), flags=cv2.INTER_LINEAR)
                        input_img = cv2.resize(rect_r, (input_height, input_height))
                        input_height, input_width = input_img.shape[:2]

                    # ズーム
                    if (float(self.capZoom) != 1):
                        zm = float(self.capZoom)
                        x1 = int((input_width-(input_width/zm))/2)
                        x2 = input_width - x1
                        y1 = int((input_height-(input_height/zm))/2)
                        y2 = input_height - y1
                        zm_img = input_img[y1:y2, x1:x2]
                        input_img = zm_img.copy()
                        input_height, input_width = input_img.shape[:2]

                    # ＦＰＳ計測
                    fps = qFPS_class.get()
                    if ((time.time() - qFPS_last) > 5):
                        qFPS_last  = time.time()

                        # 結果出力(fps)
                        out_name  = '_fps_'
                        out_value = '{:.1f}'.format(fps)
                        cn_s.put([out_name, out_value])

                        # 結果出力(reso)
                        out_name  = '_reso_'
                        out_value = str(input_width) + 'x' + str(input_height)
                        if (float(self.capZoom) != 1):
                            out_value += ' (Zoom=' + self.capZoom + ')'
                        cn_s.put([out_name, out_value])

                    # 結果出力
                    if (cn_s.qsize() == 0):
                        out_name  = '[img]'
                        out_value = input_img.copy()
                        cn_s.put([out_name, out_value])



            # アイドリング
            slow = False
            if  (qFunc.statusCheck(qBusy_dev_cpu) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_dev_scn) == True):
                slow = True
            if  (qFunc.statusCheck(qBusy_d_play   ) == True) \
            or  (qFunc.statusCheck(qBusy_d_browser) == True):
                slow = True

            if (slow == True):
                time.sleep(1.00)
            else:
                time.sleep((1/int(self.capFps))/2)

        # 終了処理
        if (True):

            # レディ解除
            qFunc.statusSet(self.fileRdy, False)

            # ビジー解除 (!ready)
            qFunc.statusSet(self.fileBsy, False)
            if (str(self.id) == '0'):
                qFunc.statusSet(qBusy_d_inp, False)

            # キュー削除
            while (cn_r.qsize() > 0):
                cn_r_get = cn_r.get()
                cn_r.task_done()
            while (cn_s.qsize() > 0):
                cn_s_get = cn_s.get()
                cn_s.task_done()

            # ログ
            qLog.log('info', self.proc_id, 'end', display=self.logDisp, )
            qFunc.statusSet(self.fileRun, False)
            self.proc_beat = None



if __name__ == '__main__':

    # 共通クラス
    qRiKi.init()
    qFunc.init()

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )

    # 設定
    cv2.namedWindow('Display', 1)
    cv2.moveWindow( 'Display', 0, 0)

    capture_thread = proc_capture(name='capture', id='0', runMode='debug', 
                                  capStretch='0', capRotate='0', capZoom='1.0', capFps='2', )
    capture_thread.begin()



    # ループ
    chktime = time.time()
    while ((time.time() - chktime) < 15):

        res_data  = capture_thread.get()
        res_name  = res_data[0]
        res_value = res_data[1]
        if (res_name != ''):
            if (res_name == '[window]'):
                pass
            elif (res_name == '[img]'):
                cv2.imshow('Display', res_value.copy() )
                cv2.waitKey(1)
            else:
                print(res_name, res_value, )

        #if (capture_thread.proc_s.qsize() == 0):
        #    capture_thread.put(['_status_', ''])

        time.sleep(0.02)

    time.sleep(1.00)
    capture_thread.abort()
    del capture_thread



    cv2.destroyAllWindows()



