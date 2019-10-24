#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://www.iplaypy.com/code/other/o2404.html

#! /usr/bin/env python
#coding=utf-8
 
import ctypes
import struct
import time
 
#winmm = ctypes.windll.winmm
 
waveOutGetVolume = (
  ctypes.windll.winmm.waveOutGetVolume)
 
waveOutSetVolume = (
  ctypes.windll.winmm.waveOutSetVolume)
 
# 最小/最大音量的常量设定
MINIMUM_VOLUME = 0     # fader control (MSDN Library)
MAXIMUM_VOLUME = 4294967295 # fader control (MSDN Library)
#调节音量 volue范围 0-100
def SetVolume(volume):
    """Set the speaker volume on the 'Volume Control' mixer"""
    if not (MINIMUM_VOLUME <= volume <= MAXIMUM_VOLUME):
        print('MIN,MAX',MINIMUM_VOLUME,MAXIMUM_VOLUME)
        raise ValueError #"Volume out of range"
 
    #按公式处理音量数值
    volume = volume * MAXIMUM_VOLUME/100;
    #设置音量
    ret = waveOutSetVolume(0, volume)
 
    if ret != 0:
        print(WindowsError, "Error %d while setting volume" % ret)
 
    return
 
if __name__ == '__main__':
    #最大音量
    SetVolume(1)
    time.sleep(5.00)
    #中等音量
    SetVolume(0.5)
    time.sleep(5.00)
    #静音
    SetVolume(0)
    time.sleep(5.00)




