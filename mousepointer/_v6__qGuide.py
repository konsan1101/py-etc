#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2022 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import os
import time

import PySimpleGUI as sg

import pyautogui
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

import platform
qPLATFORM = platform.system().lower() #windows,darwin,linux



qPath_fonts     = '_fonts/'



class qGuide_class:

    def __init__(self, ):

        # 初期化
        self.panel  = '5'
        self.title  = 'Guide_5'
        self.image  = None
        self.window = None
        self.left   = 0
        self.top    = 0
        self.width  = 320
        self.height = 240

        # フォント
        self.font_default = {'file':qPath_fonts + '_vision_font_ipaexg.ttf','offset':8}
        self.font_status  = {'file':qPath_fonts + '_vision_font_ipag.ttf',  'offset':8}
        try:
            self.font32_default  = ImageFont.truetype(self.font_default['file'], 32, encoding='unic')
            self.font32_defaulty =                    self.font_default['offset']
        except:
            self.font32_default  = None
            self.font32_defaulty = 0

    def init(self, panel='5', title='', image=None, alpha_channel=1, ):
        if (title ==''):
            title = 'Guide_' + panel
        self.panel = panel
        self.title = title

        # 表示位置
        image_height, image_width = image.shape[:2]
        if  (self.title != 'detect_face') \
        and (self.title != 'detect_speech'):
            self.left, self.top, self.width, self.height = self.getPanelPos(self.panel,)

            if (self.panel == '7') \
            or (self.panel == '8') \
            or (self.panel == '9'):
                self.top -= 50

            if (self.title.find('_guide_') >= 0):
                self.height = int(self.height/4)
                if (self.panel == '7') \
                or (self.panel == '8') \
                or (self.panel == '9'):
                    self.top += (self.height * 3)

            self.image  = cv2.resize(image, (self.width, self.height))

        elif  (self.title == 'detect_face'):
            w, h = pyautogui.size()
            chksec9 = int(time.time()) % 10
            chksec2 = int(time.time()) % 2
            self.left   = int(w * (chksec9 * 0.1))
            self.top    = int(h * (chksec2 * 0.1))
            self.top   += int(h * 0.1)
            self.width  = int(w * 0.1)
            self.height = int(self.width * image_height / image_width)
            self.image  = cv2.resize(image, (self.width, self.height))
            self.title  = 'Face_' + str(chksec9)

        elif  (self.title == 'detect_speech'):
            w, h = pyautogui.size()
            chksec5 = int(time.time()) % 5
            chksec2 = int(time.time()) % 2
            self.left   = int(w * (chksec5 * 0.2))
            self.top    = int(h * (chksec2 * 0.1))
            self.top   += int(h * 0.7)
            self.width  = int(w * 0.2)
            self.height = int(self.width * image_height / image_width)
            self.image  = cv2.resize(image, (self.width, self.height))
            self.title  = 'Speech_' + str(chksec5)

        # pySimpleGUI
        sg.theme('Black')
        sg.set_options(element_padding=(0,0), margins=(1,1), border_width=0)

        # レイアウト
        red_x = "R0lGODlhEAAQAPeQAIsAAI0AAI4AAI8AAJIAAJUAAJQCApkAAJoAAJ4AAJkJCaAAAKYAAKcAAKcCAKcDA6cGAKgAAKsAAKsCAKwAAK0AAK8AAK4CAK8DAqUJAKULAKwLALAAALEAALIAALMAALMDALQAALUAALYAALcEALoAALsAALsCALwAAL8AALkJAL4NAL8NAKoTAKwbAbEQALMVAL0QAL0RAKsREaodHbkQELMsALg2ALk3ALs+ALE2FbgpKbA1Nbc1Nb44N8AAAMIWAMsvAMUgDMcxAKVABb9NBbVJErFYEq1iMrtoMr5kP8BKAMFLAMxKANBBANFCANJFANFEB9JKAMFcANFZANZcANpfAMJUEMZVEc5hAM5pAMluBdRsANR8AM9YOrdERMpIQs1UVMR5WNt8X8VgYMdlZcxtYtx4YNF/btp9eraNf9qXXNCCZsyLeNSLd8SSecySf82kd9qqc9uBgdyBgd+EhN6JgtSIiNuJieGHhOGLg+GKhOKamty1ste4sNO+ueenp+inp+HHrebGrefKuOPTzejWzera1O7b1vLb2/bl4vTu7fbw7ffx7vnz8f///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAJAALAAAAAAQABAAAAjUACEJHEiwYEEABniQKfNFgQCDkATQwAMokEU+PQgUFDAjjR09e/LUmUNnh8aBCcCgUeRmzBkzie6EeQBAoAAMXuA8ciRGCaJHfXzUMCAQgYooWN48anTokR8dQk4sELggBhQrU9Q8evSHiJQgLCIIfMDCSZUjhbYuQkLFCRAMAiOQGGLE0CNBcZYmaRIDLqQFGF60eTRoSxc5jwjhACFWIAgMLtgUocJFy5orL0IQRHAiQgsbRZYswbEhBIiCCH6EiJAhAwQMKU5DjHCi9gnZEHMTDAgAOw=="
        layout = [[
                sg.Button('', image_data=red_x, button_color=('black', 'black'), key='-exit-', tooltip='Closes'),
                sg.Text(title),
                ],[
                sg.Image(filename='', key='image'),
                ]]

        # 定義
        self.close()
        try:
            no_titlebar = True
            if (qPLATFORM == 'darwin'):
                no_titlebar = False
            self.window = sg.Window(self.title, layout,
                            keep_on_top=True,
                            auto_size_text=False,
                            auto_size_buttons=False,
                            grab_anywhere=True,
                            no_titlebar=no_titlebar,
                            default_element_size=(12, 1),
                            default_button_element_size=(12, 1),
                            return_keyboard_events=True,
                            alpha_channel=alpha_channel,
                            use_default_focus=False,
                            finalize=True,
                            location=(self.left, self.top),
                            size=(self.width + 4, self.height + 22),
                            )
            # 更新
            if (not self.window is None):
                img = self.image.copy()
                png = cv2.imencode('.png', img)[1].tobytes()
                self.window['image'].update(data=png)

        except:
            self.window = None

        if (not self.window is None):
            return True
        else:
            return False

    def setMessage(self, txt='', ):
        try:
            if (not self.window is None):

                img = self.image.copy()

                # 文字描写
                if (txt != ''):
                    if (self.font32_default is None):
                        cv2.putText(img, txt, (5,self.height-15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,255))
                    else:
                        pil_image = self.cv2pil(img)
                        text_draw = ImageDraw.Draw(pil_image)
                        text_draw.text((10, self.height-42), txt, font=self.font32_default, fill=(255,0,255))
                        img = self.pil2cv(pil_image)

                # 更新
                png = cv2.imencode('.png', img)[1].tobytes()
                self.window['image'].update(data=png)
                self.window.refresh()
                return True

        except:
            pass
        return False

    def open(self, ):
        # 更新・表示
        #try:
        if True:
            if (not self.window is None):
                self.window.un_hide()
                self.window.refresh()
                return True
        #except:
        #    pass
        return False

    def read(self, ):
        # 読取
        #try:
        if True:
            if (not self.window is None):
                event, values = self.window.read(timeout=20, timeout_key='timeout')
                return event, values
        #except:
        #    pass
        return False, False

    def close(self, ):
        # 消去
        if (not self.window is None):
            #try:
            if True:
                self.read()
                self.window.hide()
                self.window.refresh()
            #except:
            #    pass
        return True

    def terminate(self, ):
        # 終了
        if (not self.window is None):
            #try:
            if True:
                self.read()
                self.window.close()
                del self.window
            #except:
            #    pass
        self.window = None
        return True



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



if __name__ == '__main__':

    qGuide = qGuide_class()

    img = cv2.imread('_icons/RiKi_start.png')
    qGuide.init(panel='5', title='', image=img,)
    qGuide.open()

    qGuide.setMessage(txt='', )
    time.sleep(3.00)

    qGuide.close()
    qGuide.init(panel='5', title='_guide_', image=img,)
    qGuide.setMessage(txt=u'こんにちは', )
    #qGuide.open()

    chkTime = time.time()
    while ((time.time() - chkTime) < 10):
        event, values = qGuide.read()
        if event in (None, 'Exit'):
            break

    qGuide.close()
    qGuide.terminate()


