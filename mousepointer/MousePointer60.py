#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pyautogui
import time
import datetime
import random

import _v6__qGuide
import numpy as np
import cv2

from PIL import Image, ImageDraw, ImageFont
import unicodedata
import mojimoji



# フォント
qPath_fonts   = 'C:/RiKi_assistant/_fonts/'
qFont_default = {'file':qPath_fonts + '_vision_font_ipaexg.ttf','offset':8}
qFont_status  = {'file':qPath_fonts + '_vision_font_ipag.ttf','offset':8}
qFont_zh = {'file':'C:/Windows/Fonts/msyh.ttc', 'offset':5}
qFont_ko = {'file':'C:/Windows/Fonts/batang.ttc', 'offset':10}

def in_japanese(txt=''):
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



def txt2img(txts=[], bg_color=(0,0,0), txt_color=(255,255,255), ):

    # フォント定義
    font128_default  = ImageFont.truetype(qFont_default['file'], 128, encoding='unic')
    font128_defaulty =                    qFont_default['offset']

    # キャンバス用意
    maxlen = 0
    for i in range(0, len(txts)):
        if (in_japanese(txts[i]) == True):
            lenstr = len(txts[i]) * 2
        else:
            lenstr = len(txts[i])
        if (maxlen < lenstr):
            maxlen = lenstr

    draw_height = int(10 + (128 + 10) * len(txts))
    draw_width = int(128 * (maxlen + 1))
    #bg_color = (0,0,0)
    text_img  = Image.new('RGB', (draw_width, draw_height), bg_color)
    text_draw = ImageDraw.Draw(text_img)

    #print(draw_width, draw_height)

    # 文字描写
    #txt_color = (255,255,255)
    for i in range(0, len(txts)):
        text_draw.text((128/2, (128 + 10)*i + font128_defaulty), txts[i], font=font128_default, fill=txt_color)

        #print(txts[i])

    return np.asarray(text_img)


def imgOverlay(img1_base, img2_overlay, threshold=64, ):

    # ベースサイズ取得
    img1_height, img1_width = img1_base.shape[:2]

    # リサイズ
    img2_resize = cv2.resize(img2_overlay, (img1_width, img1_height))

    # 重ね合わせ領域
    img2_gray    = cv2.cvtColor(img2_resize, cv2.COLOR_BGR2GRAY)
    ret, img2_bw = cv2.threshold(img2_gray, threshold, 255, cv2.THRESH_BINARY)
    img2_invert  = cv2.bitwise_not(img2_bw)

    # 合成
    img1 = cv2.bitwise_and(img1_base,   img1_base,   mask=img2_invert)
    img2 = cv2.bitwise_and(img2_resize, img2_resize, mask=img2_bw)
    img_out = cv2.add(img1, img2)

    #cv2.cvCopy(img_txts, img_base, img_bw)
    #cv2.cvCopy(img_txts, img_base, img_bw)

    return img_out



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
        self.lastSign   = '00:00'

        self.last_t = time.time()
        self.last_c = time.time()

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

        if ((time.time() - self.last_c) > self.waitSec):
            try:
                pyautogui.press("ctrl")
            except Exception as e:
                pass
            self.last_c = time.time()

        (x, y) = pyautogui.position()
        self.last_x = x
        self.last_y = y

        print('position', self.last_x, self.last_y)

    def check(self, ):
        nowTime = datetime.datetime.now()
        nowHHMMSS = nowTime.strftime('%H:%M:%S')
        nowHHMM   = nowTime.strftime('%H:%M')
        nowYOUBI  = nowTime.strftime('%a')
        if (nowHHMMSS < self.dayStart) \
        or (nowHHMMSS > self.dayEnd):
            if (self.startMsg == True):
                self.startMsg = False
                print('mouse pointer stop (day time)')
            return
        if  (nowHHMMSS > self.lunchStart) \
        and (nowHHMMSS < self.lunchEnd):
            if (self.startMsg == True):
                self.startMsg = False
                print('mouse pointer stop (lunch time)')
            return
        if  (nowYOUBI == 'Sat') \
        or  (nowYOUBI == 'Sun') \
        or  (nowYOUBI == '土') \
        or  (nowYOUBI == '日'):
            if (self.startMsg == True):
                self.startMsg = False
                print('mouse pointer stop (YOUBI=' & nowYOUBI & ')')
            return

        # Sign 00:00
        if (nowHHMM[-3:] == ':00'):
            if (nowHHMM != self.lastSign):
                self.lastSign = nowHHMM
                print(nowHHMM)

                # ベース画像
                img_base = cv2.imread('C:/RiKi_assistant/_icons/RiKi_base.png')
                image = img_base.copy()

                ## 文字画像
                #zen = mojimoji.han_to_zen(nowHHMM)
                #img_overlay = txt2img([zen], txt_color=(255,0,255) )
                #
                ## 合成
                #image = imgOverlay(img_base, img_overlay)

                # 直接描写
                image_height, image_width = image.shape[:2]
                cv2.putText(image, nowHHMM, (20, int(image_height*0.75)-40), cv2.FONT_HERSHEY_SIMPLEX, 5, (255,0,255), 12, cv2.LINE_AA)

                # 表示
                qGuide.init(panel='5', title='', image=image, alpha_channel=0.3, )
                qGuide.open()
                qGuide.setMessage(txt='', )
                time.sleep(3.00)
                qGuide.close()

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
            self.last_x = x
            self.last_y = y
            #self.last_t = time.time()



if __name__ == '__main__':

    qGuide = _v6__qGuide.qGuide_class()
    #qGuide.init()

    mousePointer = proc_mousePointer()
    mousePointer.init()

    while True:
        mousePointer.check()
        time.sleep(10)


