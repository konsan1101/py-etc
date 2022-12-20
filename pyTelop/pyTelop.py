#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2023 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import sys
#import os
#import time
#import datetime
#import glob

#import subprocess

import pyautogui
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

#import io

import PySimpleGUI as sg



# 共通ルーチン
import  _v6__qFunc
qFunc = _v6__qFunc.qFunc_class()



# フォント
qPath_fonts     = '_fonts/'
qFont_default = {'file':qPath_fonts + 'JF-Dot-jiskan24-2000.ttf','offset':16}
font96_default  = ImageFont.truetype(qFont_default['file'], 96, encoding='unic')
font96_defaulty =                    qFont_default['offset']

# 文字列確認
texts = ['おはようございます。', '今日もよろしくお願いします。', '明日はきっと良い日ですよ。']

maxlen = 0
for i in range(0, len(texts)):
    if (qFunc.in_japanese(texts[i]) == True):
        lenstr = len(texts[i]) * 2
    else:
        lenstr = len(texts[i])
    if (maxlen < lenstr):
        maxlen = lenstr

draw_height = int(10 + (96 + 10) * len(texts))
draw_width  = int(100 + 48 * maxlen)
text_img  = Image.new('RGB', (draw_width * 2, draw_height), (  0,  0,  0))
text_draw = ImageDraw.Draw(text_img)

for i in range(0, len(texts)):
    txt_color = (0,165,255) #GBR
    text_draw.text((24, (96 + 10)*i + font96_defaulty), texts[i], font=font96_default, fill=txt_color)

output_img = np.asarray(text_img)



runMode = 'debug'
alpha   = '0.9'


if __name__ == '__main__':

    # パラメータ
    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
    if (len(sys.argv) >= 3):
        alpha = str(sys.argv[2])

    # テーマ
    sg.theme('Black')
    sg.set_options(element_padding=(0,0), margins=(1,1), border_width=0)

    # レイアウト
    w, h = pyautogui.size()
    sg_title = 'pyTelop'
    sg_left = 0
    sg_top = 0 # h - draw_height
    sg_width = draw_width
    sg_height = draw_height
    
    #sg_no_titlebar = True
    #sg_resizable = False
    #red_x = "R0lGODlhEAAQAPeQAIsAAI0AAI4AAI8AAJIAAJUAAJQCApkAAJoAAJ4AAJkJCaAAAKYAAKcAAKcCAKcDA6cGAKgAAKsAAKsCAKwAAK0AAK8AAK4CAK8DAqUJAKULAKwLALAAALEAALIAALMAALMDALQAALUAALYAALcEALoAALsAALsCALwAAL8AALkJAL4NAL8NAKoTAKwbAbEQALMVAL0QAL0RAKsREaodHbkQELMsALg2ALk3ALs+ALE2FbgpKbA1Nbc1Nb44N8AAAMIWAMsvAMUgDMcxAKVABb9NBbVJErFYEq1iMrtoMr5kP8BKAMFLAMxKANBBANFCANJFANFEB9JKAMFcANFZANZcANpfAMJUEMZVEc5hAM5pAMluBdRsANR8AM9YOrdERMpIQs1UVMR5WNt8X8VgYMdlZcxtYtx4YNF/btp9eraNf9qXXNCCZsyLeNSLd8SSecySf82kd9qqc9uBgdyBgd+EhN6JgtSIiNuJieGHhOGLg+GKhOKamty1ste4sNO+ueenp+inp+HHrebGrefKuOPTzejWzera1O7b1vLb2/bl4vTu7fbw7ffx7vnz8f///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAJAALAAAAAAQABAAAAjUACEJHEiwYEEABniQKfNFgQCDkATQwAMokEU+PQgUFDAjjR09e/LUmUNnh8aBCcCgUeRmzBkzie6EeQBAoAAMXuA8ciRGCaJHfXzUMCAQgYooWN48anTokR8dQk4sELggBhQrU9Q8evSHiJQgLCIIfMDCSZUjhbYuQkLFCRAMAiOQGGLE0CNBcZYmaRIDLqQFGF60eTRoSxc5jwjhACFWIAgMLtgUocJFy5orL0IQRHAiQgsbRZYswbEhBIiCCH6EiJAhAwQMKU5DjHCi9gnZEHMTDAgAOw=="
    #layout = [[
    #        sg.Button('', image_data=red_x, button_color=('black', 'black'), key='-exit-', tooltip='Closes'),
    #        sg.Text(sg_title),
    #        ],[
    #        sg.Image(filename='', key='image'),
    #        ]]
    sg_no_titlebar = False
    sg_resizable = True
    layout = [[
            sg.Image(filename='', key='image'),
            ]]
    
    # ウィンドウ作成
    sg_win = sg.Window(sg_title, layout,
                        keep_on_top=True,
                        auto_size_text=False,
                        auto_size_buttons=False,
                        grab_anywhere=True,
                        no_titlebar=sg_no_titlebar,
                        default_element_size=(12, 1),
                        default_button_element_size=(12, 1),
                        return_keyboard_events=True,
                        alpha_channel=float(alpha),
                        use_default_focus=False,
                        finalize=True,
                        location=(sg_left, sg_top),
                        size=(sg_width + 4, sg_height + 22),
                        resizable=sg_resizable,
                        )

    # イベントループ
    kaishi = 0
    while True:

        # 文字切り出し
        img = output_img[ 0:draw_height, kaishi:kaishi+draw_width]

        # 表示
        imgbytes = cv2.imencode('.png', img)[1].tobytes() 
        sg_win['image'].update(data=imgbytes)

        # イベント確認
        if (kaishi == 0):
            timeout = 2000
        else:
            timeout = 1
        event, values = sg_win.read(timeout=timeout, timeout_key='timeout')
        # ウィンドウの×ボタンクリックで終了
        if event == sg.WIN_CLOSED:
            break
        if event in (None, '-exit-'):
            break

        kaishi += 2
        if (kaishi >= draw_width):
            kaishi = 0

        #time.sleep(0.01)

    # 終了処理
    sg_win.close()


