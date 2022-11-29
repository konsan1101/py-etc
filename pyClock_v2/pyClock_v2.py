#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2022 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------



import sys
import os
import time
import datetime
import glob

import subprocess

import pyautogui
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

import matplotlib.pyplot as plt
import io

import PySimpleGUI as sg



# 共通ルーチン
import  _v6__qFunc
qFunc = _v6__qFunc.qFunc_class()



qPath_fonts     = '_fonts/'
qPath_config    = '_config/'
qPath_task      = '_task/'
qPath_0_all     = qPath_config + qPath_task + '0_all/'
qPath_0_week    = qPath_config + qPath_task + '0_week/'
qPath_1_mon     = qPath_config + qPath_task + '1_mon/'
qPath_2_tue     = qPath_config + qPath_task + '2_tue/'
qPath_3_wed     = qPath_config + qPath_task + '3_wed/'
qPath_4_thu     = qPath_config + qPath_task + '4_thu/'
qPath_5_fri     = qPath_config + qPath_task + '5_fri/'
qPath_6_sat     = qPath_config + qPath_task + '6_sat/'
qPath_7_sun     = qPath_config + qPath_task + '7_sun/'



runMode = 'analog'
#runMode = 'digital'
panel   = 'auto'
design  = 'auto'
alpha   = '0.7'



def task_check(yymmdd='20221101', hhmm='0000', youbi='Mon', ):
    if (True):
        task_execute(path=qPath_0_all,  yymmdd=yymmdd, hhmm=hhmm, youbi=youbi, )
    if (youbi=='Mon' or youbi=='Tue' or youbi=='Wed' or youbi=='Thu' or youbi=='Fri'):
        task_execute(path=qPath_0_week, yymmdd=yymmdd, hhmm=hhmm, youbi=youbi, )
    if (youbi=='Mon'):
        task_execute(path=qPath_1_mon,  yymmdd=yymmdd, hhmm=hhmm, youbi=youbi, )
    if (youbi=='Tue'):
        task_execute(path=qPath_2_tue,  yymmdd=yymmdd, hhmm=hhmm, youbi=youbi, )
    if (youbi=='Wed'):
        task_execute(path=qPath_3_wed,  yymmdd=yymmdd, hhmm=hhmm, youbi=youbi, )
    if (youbi=='Thu'):
        task_execute(path=qPath_4_thu,  yymmdd=yymmdd, hhmm=hhmm, youbi=youbi, )
    if (youbi=='Fri'):
        task_execute(path=qPath_5_fri,  yymmdd=yymmdd, hhmm=hhmm, youbi=youbi, )
    if (youbi=='Sat'):
        task_execute(path=qPath_6_sat,  yymmdd=yymmdd, hhmm=hhmm, youbi=youbi, )
    if (youbi=='Sun'):
        task_execute(path=qPath_7_sun,  yymmdd=yymmdd, hhmm=hhmm, youbi=youbi, )
        
    path_dirs = glob.glob(qPath_config + qPath_task + yymmdd + '*')
    if (len(path_dirs) > 0):
        path_dirs.sort()
        for p in path_dirs:
            if (os.path.isdir(p)):
                pa = p.replace('\\','/') + '/'
                task_execute(path=pa, yymmdd=yymmdd, hhmm=hhmm, youbi=youbi, )



def task_execute(path='', yymmdd='20221101', hhmm='0000', youbi='Mon', ):
    #print(path, yymmdd, hhmm, youbi, )

    path_files = glob.glob(path + hhmm + '*.*')
    if (len(path_files) > 0):
        path_files.sort()
        for f in path_files:
            if (os.path.isfile(f)):
                ext=f[-4:].lower()
                print(f,ext)

                if (ext=='.wav') or (ext=='.mp3'):
                    file = f.replace('/','\\')
                    sox=subprocess.Popen(['sox', '-q', file, '-d', 
                        ], \
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                if (ext=='.mp4'):
                    file = f.replace('/','\\')
                    ffplay = subprocess.Popen(['ffplay', '-i', file, \
                        '-noborder', '-autoexit', \
                        '-loglevel', 'warning', \
                        ], \
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

                if (ext=='.bat'):
                    file = f.replace('/','\\')
                    cmd = subprocess.Popen(['cmd.exe', '/c', file, \
                        ], \
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, )



class qClock_class:

    def __init__(self, ):

        # フォント
        self.font_dseg7 = {'file':qPath_fonts + 'DSEG7Classic-Bold.ttf','offset':8}
        try:
            self.font32_dseg7 = ImageFont.truetype(self.font_dseg7['file'], 32, encoding='unic')
            self.font32_dseg7y =                   self.font_dseg7['offset']
            self.font99_dseg7 = ImageFont.truetype(self.font_dseg7['file'], 192, encoding='unic')
            self.font99_dseg7y =                   self.font_dseg7['offset']
            self.font88_dseg7 = ImageFont.truetype(self.font_dseg7['file'], 288, encoding='unic')
            self.font88_dseg7y =                   self.font_dseg7['offset']
        except:
            self.font32_dseg7  = None
            self.font32_dseg7y = 0
            self.font99_dseg7  = None
            self.font99_dseg7y = 0
            self.font88_dseg7  = None
            self.font88_dseg7y = 0

        # 規定値
        self.analog_b_fcolor = 'white'
        self.analog_b_tcolor = 'fuchsia'
        self.analog_b_bcolor = 'black'
        self.analog_s_fcolor  = 'red'
        self.analog_s_bcolor1 = 'darkred'
        self.analog_s_bcolor2 = 'tomato'
        self.analog_m_fcolor  = 'cyan'
        self.analog_m_bcolor1 = 'darkgreen'
        self.analog_m_bcolor2 = 'limegreen'
        self.analog_h_fcolor  = 'cyan'
        self.analog_h_bcolor1 = 'darkblue'
        self.analog_h_bcolor2 = 'deepskyblue'

        self.digital_b_fcolor = 'white'
        self.digital_b_tcolor = 'fuchsia'
        self.digital_b_bcolor = 'black'

        # -------------
        # アナログ時計盤
        # -------------
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(10,10))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(-1.05,1.05)
        self.ax.set_ylim(-1.05,1.05)
        self.ax.axis('off')
        # 外周
        vals = np.array([100,])
        colors = [self.analog_b_fcolor,]
        self.ax.pie(vals,colors=colors,counterclock=False, startangle=90, radius=1, wedgeprops=dict(width=0.02), )
        # 目盛
        for t in range(1,60):
            t_x1 = np.sin(np.radians(t/60*360)) * 0.95
            t_x2 = np.sin(np.radians(t/60*360)) * 0.98
            t_y1 = np.cos(np.radians(t/60*360)) * 0.95
            t_y2 = np.cos(np.radians(t/60*360)) * 0.98
            self.ax.plot([t_x1,t_x2],[t_y1,t_y2],color=self.analog_b_fcolor, lw=1,)
        for t in range(1,13):
            t_x1 = np.sin(np.radians((t % 12)/12*360)) * 0.90
            t_x2 = np.sin(np.radians((t % 12)/12*360)) * 0.98
            t_y1 = np.cos(np.radians((t % 12)/12*360)) * 0.90
            t_y2 = np.cos(np.radians((t % 12)/12*360)) * 0.98
            self.ax.plot([t_x1,t_x2],[t_y1,t_y2],color=self.analog_b_fcolor, lw=3,)
        # 画像保存
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, )
        enc = np.frombuffer(buf.getvalue(), dtype=np.uint8)
        self.analog_base   = cv2.imdecode(enc, 1)
        self.analog_height = self.analog_base.shape[0]
        self.analog_width  = self.analog_base.shape[1]
        
        # -------------
        # デジタル時計盤
        # -------------
        width  = 750
        height = 270
        self.digital_base = np.zeros((height,width,3), np.uint8)
        if (self.digital_b_bcolor == 'white'):
            cv2.rectangle(self.digital_dseg7_0,(0,0),(width,height),(255,255,255),thickness=-1,)
        if (self.font32_dseg7 is None):
            pass
        else:
            hhmm = '{:02d}:{:02d}'.format(int(88), int(88))
            pil_image = qFunc.cv2pil(self.digital_base)
            text_draw = ImageDraw.Draw(pil_image)
            if (self.digital_b_bcolor == 'white'):
                text_draw.text((int(width*0.05),int(height*0.2)), hhmm, font=self.font99_dseg7, fill=(240,240,240))
            else:
                text_draw.text((int(width*0.05),int(height*0.2)), hhmm, font=self.font99_dseg7, fill=(16,16,16))
            self.digital_base = qFunc.pil2cv(pil_image)

        self.last_hhmm = ''



    def getImage_digital(self, dt_now, design=0, ):
        yy = dt_now.year
        mm = dt_now.month
        dd = dt_now.day
        h = dt_now.hour
        m = dt_now.minute
        s = dt_now.second

        width  = self.digital_base.shape[1]
        height = self.digital_base.shape[0]

        #----------
        # デジタル
        #----------
        ymd  = '{:04d}.{:02d}.{:02d}'.format(yy, mm, dd)
        hhmm = '{:02d}:{:02d}'.format(int(h), int(m))
        if (hhmm != self.last_hhmm):
            self.last_hhmm = hhmm
            
            self.digital_dseg7_0 = np.zeros((height,width,3), np.uint8)
            if (self.font32_dseg7 is None):
                cv2.putText(self.digital_dseg7_0, ymd, (int(width*0.27),int(height*0.2)), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,0,0))
                cv2.putText(self.digital_dseg7_0, hhmm, (int(width*0.10),int(height*0.85)), cv2.FONT_HERSHEY_TRIPLEX, 7, (255,0,255))
                self.digital_dseg7_1 = self.digital_dseg7_0.copy()
            else:
                hhmm2 = '{:02d} {:02d}'.format(int(h), int(m))

                pil_image1 = qFunc.cv2pil(self.digital_dseg7_0)
                pil_image2 = qFunc.cv2pil(self.digital_dseg7_0)
                text_draw1 = ImageDraw.Draw(pil_image1)
                text_draw1.text((int(width*0.63),int(height*0.05)), ymd, font=self.font32_dseg7, fill=(0,0,255))
                text_draw1.text((int(width*0.05),int(height*0.2)), hhmm, font=self.font99_dseg7, fill=self.digital_b_tcolor)
                text_draw2 = ImageDraw.Draw(pil_image2)
                text_draw2.text((int(width*0.63),int(height*0.05)), ymd, font=self.font32_dseg7, fill=(0,0,255))
                text_draw2.text((int(width*0.05),int(height*0.2)), hhmm2, font=self.font99_dseg7, fill=self.digital_b_tcolor)
                self.digital_dseg7_0 = qFunc.pil2cv(pil_image1)
                self.digital_dseg7_1 = qFunc.pil2cv(pil_image2)

        # 秒針
        if ((s % 2) == 0):
            img = self.digital_dseg7_0.copy()
        else:
            img = self.digital_dseg7_1.copy()
        w = int(width * (s/60))
        cv2.rectangle(img,(0,0),(w,2),(0,0,255),thickness=-1,)

        #----------
        # 画像合成
        #----------
        base = self.digital_base        
        over = img
        # 表側でマスク作成
        gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)    
        # 表側,裏側,合成
        fg = cv2.bitwise_and(over, over, mask = mask)
        bg = cv2.bitwise_and(base, base, mask = mask_inv)
        img = cv2.add(bg, fg)

        return img

    def getImage_analog(self, dt_now, design=0, ):
        yy = dt_now.year
        mm = dt_now.month
        dd = dt_now.day
        h = dt_now.hour
        m = dt_now.minute
        s = dt_now.second

        m = m + s/60
        h = h + m/60

        #----------
        # デジタル
        #----------
        ymd  = '{:04d}.{:02d}.{:02d}'.format(yy, mm, dd)
        hhmm = '{:02d}:{:02d}'.format(int(h), int(m))
        if (hhmm != self.last_hhmm):
            self.last_hhmm = hhmm
            
            width  = self.analog_width
            height = self.analog_height
            self.analog_dseg7_0 = np.zeros((height,width,3), np.uint8)
            if (self.font32_dseg7 is None):
                cv2.putText(self.analog_dseg7_0, ymd, (int(width*0.27),int(height*0.33)), cv2.FONT_HERSHEY_TRIPLEX, 2, (255,0,0))
                cv2.putText(self.analog_dseg7_0, hhmm, (int(width*0.2),int(height*0.7)), cv2.FONT_HERSHEY_TRIPLEX, 5, (255,0,255))
                self.analog_dseg7_1 = self.analog_dseg7_0.copy()
            else:
                if ((design % 2) == 0):
                    hhmm2 = '{:02d} {:02d}'.format(int(h), int(m))
                    pil_image1 = qFunc.cv2pil(self.analog_dseg7_0)
                    pil_image2 = qFunc.cv2pil(self.analog_dseg7_0)
                    text_draw1 = ImageDraw.Draw(pil_image1)
                    text_draw1.text((int(width*0.37),int(height*0.30)), ymd, font=self.font32_dseg7, fill=(0,0,255))
                    text_draw1.text((int(width*0.06),int(height*0.6)), hhmm, font=self.font99_dseg7, fill=self.analog_b_tcolor)
                    text_draw2 = ImageDraw.Draw(pil_image2)
                    text_draw2.text((int(width*0.37),int(height*0.30)), ymd, font=self.font32_dseg7, fill=(0,0,255))
                    text_draw2.text((int(width*0.06),int(height*0.6)), hhmm2, font=self.font99_dseg7, fill=self.analog_b_tcolor)
                    self.analog_dseg7_0 = qFunc.pil2cv(pil_image1)
                    self.analog_dseg7_1 = qFunc.pil2cv(pil_image2)
                else:
                    hh = '{:02d}'.format(int(h))
                    mm = '{:02d}'.format(int(m))
                    pil_image = qFunc.cv2pil(self.analog_dseg7_0)
                    text_draw = ImageDraw.Draw(pil_image)
                    text_draw.text((int(width*0.65),int(height*0.02)), ymd, font=self.font32_dseg7, fill=(0,0,255))
                    text_draw.text((int(width*0.05),int(height*0.08)), hh, font=self.font88_dseg7, fill=self.analog_b_tcolor)
                    text_draw.text((int(width*0.35),int(height*0.53)), mm, font=self.font88_dseg7, fill=self.analog_b_tcolor)
                    self.analog_dseg7_0 = qFunc.pil2cv(pil_image)
                    self.analog_dseg7_1 = self.analog_dseg7_0.copy()

        # 文字 2 パターン
        # 盤 3 パターン
        # 素数 5 目盛
        # 素数 7 パイ配色
        # 素数 11 目盛文字

        #----------
        # パイ盤 0,1
        #----------
        if ((design % 3) == 0) \
        or ((design % 3) == 1):
            plt.cla()
            # 外周
            vals = np.array([100,])
            colors = [self.analog_b_bcolor,]
            self.ax.pie(vals,colors=colors,counterclock=False, startangle=90, radius=1, wedgeprops=dict(width=0.02), )
            # 色
            if ((design % 3) == 1) \
            or ((design % 7) == 4):
                s_colors = [self.analog_s_bcolor2, self.analog_s_bcolor1,]
                m_colors = [self.analog_m_bcolor2, self.analog_m_bcolor1,]
                h_colors = [self.analog_h_bcolor2, self.analog_h_bcolor1,]
            else:
                s_colors = [self.analog_s_bcolor1, self.analog_b_bcolor,]
                m_colors = [self.analog_m_bcolor1, self.analog_b_bcolor,]
                h_colors = [self.analog_h_bcolor1, self.analog_b_bcolor,]
            # 秒
            vals = np.array([s/60, 1-s/60,])
            self.ax.pie(vals,colors=s_colors,counterclock=False, startangle=90, radius=0.85, wedgeprops=dict(width=0.2), )
            # 分
            vals = np.array([m/60, 1-m/60,])
            self.ax.pie(vals,colors=m_colors,counterclock=False, startangle=90, radius=0.60, wedgeprops=dict(width=0.2), )
            # 時
            vals = np.array([(h % 12)/12, 1-(h % 12)/12,])
            self.ax.pie(vals,colors=h_colors,counterclock=False, startangle=90, radius=0.35, wedgeprops=dict(width=0.2), )
            # 目盛
            if ((design % 11) != 1):
                for t in range(1,13):
                    if ((t % 3)==0):
                        t_x = np.sin(np.radians((t % 12)/12*360)) * 0.75
                        t_y = np.cos(np.radians((t % 12)/12*360)) * 0.75
                        self.ax.text(t_x, t_y, str(t), color=self.analog_b_fcolor, ha='center', va='center', size=64, )
            # 画像保存
            buf = io.BytesIO()
            self.fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, )
            enc = np.frombuffer(buf.getvalue(), dtype=np.uint8)
            img_pie = cv2.imdecode(enc, 1)
            # サイズ調整
            if (img_pie.shape) != (self.analog_base.shape):
                img_pie = cv2.resize(img_pie, (self.analog_width, self.analog_height))
            #plt.show()

        #----------
        # 画像合成
        #----------
        if ((design % 3) == 1):

            if ((design % 5) == 1):
                base = img_pie.copy()
            else:
                base = img_pie
                over = self.analog_base        
                # 表側でマスク作成
                gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)    
                # 表側,裏側,合成
                fg = cv2.bitwise_and(over, over, mask = mask)
                bg = cv2.bitwise_and(base, base, mask = mask_inv)
                base = cv2.add(bg, fg)

            if ((s % 2) == 0):
                over = self.analog_dseg7_0
            else:
                over = self.analog_dseg7_1
            # 表側でマスク作成
            gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)    
            # 表側,裏側,合成
            fg = cv2.bitwise_and(over, over, mask = mask)
            bg = cv2.bitwise_and(base, base, mask = mask_inv)
            img = cv2.add(bg, fg)

            return img

        #----------
        # アナログ盤 0,2
        #----------
        if ((design % 3) == 0) \
        or ((design % 3) == 2):
            plt.cla()
            # 外周
            vals = np.array([100,])
            colors = [self.analog_b_bcolor,]
            self.ax.pie(vals,colors=colors,counterclock=False, startangle=90, radius=1, wedgeprops=dict(width=0.02), )
            # 目盛
            if ((design % 11) != 1):
                for t in range(1,13):
                    if ((t % 3)==0):
                        t_x = np.sin(np.radians((t % 12)/12*360)) * 0.75
                        t_y = np.cos(np.radians((t % 12)/12*360)) * 0.75
                        self.ax.text(t_x, t_y, str(t), color=self.analog_b_fcolor, ha='center', va='center', size=64, )
            # 時針
            h_x = np.sin(np.radians((h % 12)/12*360)) * 0.55
            h_y = np.cos(np.radians((h % 12)/12*360)) * 0.55
            self.ax.plot([0,h_x], [0,h_y], color=self.analog_h_fcolor, lw=32, zorder=99, )
            # 分針
            m_x = np.sin(np.radians(m/60*360)) * 0.80
            m_y = np.cos(np.radians(m/60*360)) * 0.80
            self.ax.plot([0,m_x], [0,m_y], color=self.analog_m_fcolor, lw=16, zorder=99, )
            # 秒針
            s_x = np.sin(np.radians(s/60*360)) * 0.85
            s_y = np.cos(np.radians(s/60*360)) * 0.85
            self.ax.plot([0,s_x], [0,s_y], color=self.analog_s_fcolor, lw=8, zorder=99, )
            # 画像保存
            buf = io.BytesIO()
            self.fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, )
            enc = np.frombuffer(buf.getvalue(), dtype=np.uint8)
            img_line = cv2.imdecode(enc, 1)
            # サイズ調整
            if (img_line.shape) != (self.analog_base.shape):
                img_line = cv2.resize(img_line, (self.analog_width, self.analog_height))
            #plt.show()

        #----------
        # 画像合成
        #----------
        if ((design % 3) == 2):

            if ((design % 5) == 1):
                if ((s % 2) == 0):
                    base = self.analog_dseg7_0.copy()
                else:
                    base = self.analog_dseg7_1.copy()
            else:
                base = self.analog_base
                if ((s % 2) == 0):
                    over = self.analog_dseg7_0
                else:
                    over = self.analog_dseg7_1
                # 表側でマスク作成
                gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)    
                # 表側,裏側,合成
                fg = cv2.bitwise_and(over, over, mask = mask)
                bg = cv2.bitwise_and(base, base, mask = mask_inv)
                base = cv2.add(bg, fg)

            over = img_line
            # 表側でマスク作成
            gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)    
            # 表側,裏側,合成
            fg = cv2.bitwise_and(over, over, mask = mask)
            bg = cv2.bitwise_and(base, base, mask = mask_inv)
            img = cv2.add(bg, fg)

            return img

        #----------
        # 画像合成
        #----------
        if True:
            base = img_pie
            if ((s % 2) == 0):
                over = self.analog_dseg7_0
            else:
                over = self.analog_dseg7_1
            # 表側でマスク作成
            gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)    
            # 表側,裏側,合成
            fg = cv2.bitwise_and(over, over, mask = mask)
            bg = cv2.bitwise_and(base, base, mask = mask_inv)
            base = cv2.add(bg, fg)

            if ((design % 5) != 1):
                over = self.analog_base
                # 表側でマスク作成
                gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
                ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
                mask_inv = cv2.bitwise_not(mask)    
                # 表側,裏側,合成
                fg = cv2.bitwise_and(over, over, mask = mask)
                bg = cv2.bitwise_and(base, base, mask = mask_inv)
                base = cv2.add(bg, fg)

            over = img_line
            # 表側でマスク作成
            gray = cv2.cvtColor(over, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)    
            # 表側,裏側,合成
            fg = cv2.bitwise_and(over, over, mask = mask)
            bg = cv2.bitwise_and(base, base, mask = mask_inv)
            img = cv2.add(bg, fg)

        return img



if __name__ == '__main__':

    # 初期化
    qClock = qClock_class()

    qFunc.makeDirs(qPath_0_all,  remove=False, )
    qFunc.makeDirs(qPath_0_week, remove=False, )
    qFunc.makeDirs(qPath_1_mon,  remove=False, )
    qFunc.makeDirs(qPath_2_tue,  remove=False, )
    qFunc.makeDirs(qPath_3_wed,  remove=False, )
    qFunc.makeDirs(qPath_4_thu,  remove=False, )
    qFunc.makeDirs(qPath_5_fri,  remove=False, )
    qFunc.makeDirs(qPath_6_sat,  remove=False, )
    qFunc.makeDirs(qPath_7_sun,  remove=False, )

    # パラメータ
    if (len(sys.argv) >= 2):
        runMode  = str(sys.argv[1]).lower()
    if (len(sys.argv) >= 3):
        panel  = str(sys.argv[2])
    if (len(sys.argv) >= 4):
        design = str(sys.argv[3])
    if (len(sys.argv) >= 5):
        alpha = str(sys.argv[4])

    # テーマ
    sg.theme('Black')
    sg.set_options(element_padding=(0,0), margins=(1,1), border_width=0)

    # レイアウト
    w, h = pyautogui.size()
    sg_title = 'pyClock'
    if (panel == 'auto'):
        if (runMode != 'digital'):
            sg_left = w - int(w/3)
            sg_top = 0
            sg_width = int(w/3)
            sg_height = int(w/3)
        else:
            sg_left = w - int(w/3)
            sg_top = 0
            sg_width = int(w/3)
            sg_height = int(h/3)
    else:
        sg_left, sg_top, sg_width, sg_height = qFunc.getPanelPos(id=panel)
    
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
    bk_s = 0
    bk_m = 0
    while True:
        # イベントの読み込み
        event, values = sg_win.read(timeout=200, timeout_key='timeout')
        # ウィンドウの×ボタンクリックで終了
        if event == sg.WIN_CLOSED:
            break
        if event in (None, '-exit-'):
            break

        # サイズ変更対応
        w, h = sg_win.size
        sg_width = w - 4
        sg_height = h - 22

        # 時計表示
        dt_now    = datetime.datetime.now()
        dt_YYMMDD = dt_now.strftime('%Y%m%d')
        dt_YOUBI  = dt_now.strftime('%a')
        dt_HHMM   = dt_now.strftime('%H%M')
        dt_YYYYMMDDHHMM  = dt_now.strftime('%H%M')
        s = dt_now.second
        m = dt_now.minute
        h = dt_now.hour
        if (s != bk_s):
            bk_s=s

            # デザイン
            d = h*60+m
            if (design != 'auto'):
                try:
                    d = int(design)
                except:
                    d = 0

            # アナログ時計
            if (runMode != 'digital'):
                img = qClock.getImage_analog(dt_now, d)
                img = cv2.resize(img, (sg_width,sg_height))

            # デジタル時計
            else:
                img = qClock.getImage_digital(dt_now, d)
                img = cv2.resize(img, (sg_width,sg_height))

            imgbytes = cv2.imencode('.png', img)[1].tobytes() 
            sg_win['image'].update(data=imgbytes)

        if (m != bk_m):
            bk_m=m
            task_check(dt_YYMMDD, dt_HHMM, dt_YOUBI, )



    # 終了処理
    sg_win.close()


