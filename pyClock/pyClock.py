#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://qiita.com/ddside/items/5831980e9409e2b09ed5

import sys
import os
import datetime
if (os.name == 'nt'):
    import win32gui
    import win32con

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

import pyautogui

w, h = pyautogui.size()

win_title = 'pyClock'
win_size = int(h * 0.006) * 100 #800
win = pg.GraphicsLayoutWidget(show=True, title=win_title, )
win.resize(win_size, win_size)

pg.setConfigOptions(antialias=True)

graph = win.addPlot()
graph.showAxis('bottom', False)
graph.showAxis('left', False)
graph.setAspectLocked(lock=True)
graph.setMouseEnabled(x=False, y=False)

radius = 1
font_size = int(win_size / 10) #64

# 日付・時刻

font = QtGui.QFont()
font.setPixelSize(int(font_size / 1.0))
date_text = pg.TextItem(text='0000.00.00', anchor=(0.5, 0.5), color=(0,0,255), )
date_text.setPos(0, radius / 2.5)
date_text.setFont(font)
graph.addItem(date_text)

font = QtGui.QFont('DSEG7 Classic')
font.setPixelSize(int(font_size / 0.5))
time_text = pg.TextItem(text='00:00', anchor=(0.5, 0.5), color=(255,0,255), )
time_text.setPos(0, -radius / 2.5)
time_text.setFont(font)
graph.addItem(time_text)


# 円周

x = radius * np.cos(np.linspace(0, 2 * np.pi, 1000))
y = radius * np.sin(np.linspace(0, 2 * np.pi, 1000))
graph.plot(x, y, pen=pg.mkPen(width=6,color=(255,255,255)))

# 目盛（秒）

for second in range(60):
    line_length = 0.1 if second % 5 == 0 else 0.05
    line_width = 4 if second % 5 == 0 else 2
    x1 = np.sin(np.radians(360 * (second / 60))) * radius
    x2 = np.sin(np.radians(360 * (second / 60))) * (radius - line_length)
    y1 = np.cos(np.radians(360 * (second / 60))) * radius
    y2 = np.cos(np.radians(360 * (second / 60))) * (radius - line_length)
    pen = pg.mkPen(width=line_width,color=(255,255,255))
    pen.setCapStyle(QtCore.Qt.RoundCap)
    graph.plot([x1, x2], [y1, y2], pen=pen)

# 目盛（時刻）・時刻文字

hour_texts = []
for hour in range(1, 13, 1):
    x = np.sin(np.radians(360 * (hour / 12))) * radius * 0.8
    y = np.cos(np.radians(360 * (hour / 12))) * radius * 0.8
    hour_text = pg.TextItem(text=str(hour), anchor=(0.5, 0.5), color=(255,255,255), )
    hour_text.setPos(x, y)
    font = QtGui.QFont()
    font.setPixelSize(font_size)
    hour_text.setFont(font)
    graph.addItem(hour_text)
    hour_texts.append(hour_text)

# 針（時、分、秒）

pen = pg.mkPen(width=24,color=(0,255,255))
pen.setCapStyle(QtCore.Qt.RoundCap)
hour_hand_plot = graph.plot(pen=pen)

pen = pg.mkPen(width=12,color=(0,255,255))
pen.setCapStyle(QtCore.Qt.RoundCap)
minute_hand_plot = graph.plot(pen=pen)

pen = pg.mkPen(width=6,color=(255,0,0))
pen.setCapStyle(QtCore.Qt.RoundCap)
second_hand_plot = graph.plot(pen=pen)



def resize_text():
    size = win.size()
    height = size.height()
    width = size.width()
    new_font_size = font_size * (min(height, width) / win_size)

    font = QtGui.QFont()
    font.setPixelSize(int(new_font_size / 1.0))
    date_text.setFont(font)

    font = QtGui.QFont('DSEG7 Classic')
    font.setPixelSize(int(new_font_size / 0.5))
    time_text.setFont(font)

    for hour_text in hour_texts:
        font = QtGui.QFont()
        font.setPixelSize(int(new_font_size))
        hour_text.setFont(font)



def set_datetime():
    dt_now = datetime.datetime.now()
    yy = dt_now.year
    mm = dt_now.month
    dd = dt_now.day
    h = dt_now.hour
    m = dt_now.minute
    s = dt_now.second

    deg_second = (s / 60) * 360
    deg_minute = (m / 60) * 360 + (1 / 60) * 360 * (s / 60)
    deg_hour = (h / 12) * 360 + (1 / 12) * 360 * (m / 60)

    second_hand_length = 0.85
    minute_hand_length = 0.8
    hour_hand_length = 0.5

    x_second = np.sin(np.radians(deg_second)) * radius * second_hand_length
    y_second = np.cos(np.radians(deg_second)) * radius * second_hand_length
    second_hand_plot.setData([0, x_second], [0, y_second])

    x_minute = np.sin(np.radians(deg_minute)) * radius * minute_hand_length
    y_minute = np.cos(np.radians(deg_minute)) * radius * minute_hand_length
    minute_hand_plot.setData([0, x_minute], [0, y_minute])

    x_hour = np.sin(np.radians(deg_hour)) * radius * hour_hand_length
    y_hour = np.cos(np.radians(deg_hour)) * radius * hour_hand_length
    hour_hand_plot.setData([0, x_hour], [0, y_hour])

    date_str = '{:04d}.{:02d}.{:02d}'.format(yy, mm, dd)
    date_text.setText(date_str)

    time_str = '{:02d}:{:02d}'.format(h, m)
    time_text.setText(time_str)

    #win.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    if (os.name == 'nt'):
        hwnd = win32gui.FindWindow(None, win_title)
        if (hwnd != False):
            #ctypes.windll.user32.SetWindowPos(parent_handle, HWND_TOP, 0, 0, width, height, SWP_SHOWWINDOW)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            #print('top')



resize_timer = QtCore.QTimer()
resize_timer.timeout.connect(resize_text)
resize_timer.start(500)

update_timer = QtCore.QTimer()
update_timer.timeout.connect(set_datetime)
update_timer.start(100)

if __name__ == '__main__':

    app = QtGui.QApplication([])

    # 右上
    w, h = pyautogui.size()
    win.move(w - win_size, 0)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
