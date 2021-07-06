#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import unicodedata
import numpy as np
import cv2
import time

# フォント
qPath_fonts   = 'C:/RiKi_assistant/_fonts/'
qFont_default = {'file':qPath_fonts + '_vision_font_ipaexg.ttf','offset':8}
qFont_status  = {'file':qPath_fonts + '_vision_font_ipag.ttf','offset':8}
qFont_zh = {'file':'C:/Windows/Fonts/msyh.ttc', 'offset':5}
qFont_ko = {'file':'C:/Windows/Fonts/batang.ttc', 'offset':10}

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

def txt2img(txts=[], bg_color=(0,0,0), txt_color=(255,255,255), ):

    # フォント定義
    font32_default  = ImageFont.truetype(qFont_default['file'], 32, encoding='unic')
    font32_defaulty =                    qFont_default['offset']

    # キャンバス用意
    maxlen = 0
    for i in range(0, len(txts)):
        if (in_japanese(txts[i]) == True):
            lenstr = len(txts[i]) * 2
        else:
            lenstr = len(txts[i])
        if (maxlen < lenstr):
            maxlen = lenstr

    draw_height = int(10 + (32 + 10) * len(txts))
    draw_width = int(32 + 32 * maxlen)
    #bg_color = (0,0,0)
    text_img  = Image.new('RGB', (draw_width, draw_height), bg_color)
    text_draw = ImageDraw.Draw(text_img)

    #print(draw_width, draw_height)

    # 文字描写
    #txt_color = (255,255,255)
    for i in range(0, len(txts)):
        text_draw.text((16, (32 + 10)*i + font32_defaulty), txts[i], font=font32_default, fill=txt_color)

        #print(txts[i])

    return np.asarray(text_img)



if __name__ == "__main__":

    #txts = [u'こんにちは', u'はじめまして']
    txts = ['１２：３０']

    out_image = txt2img(txts)

    cv2.imshow('Display', out_image)
    cv2.waitKey(1)
    time.sleep(5)


