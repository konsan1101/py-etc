#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://monomonotech.jp/kurage/raspberrypi/python_vlc.html
# http://www.olivieraubert.net/vlc/python-ctypes/doc/vlc.MediaPlayer-class.html

import vlc
import time

vlc_instance = vlc.Instance()
  
# creating a new media
media = vlc_instance.media_new('C:/Users/Public/BGM/BGM_Ghibli.mp4')
#media = vlc_instance.media_new('https://www.youtube.com/watch?v=pbqbnSQ5pxw')
#media = vlc_instance.media_new('_drive.mp4')

vlc_player = vlc_instance.media_player_new()
  
vlc_player.set_media(media)

vlc_player.audio_set_volume(50)
vlc_player.play()

time.sleep(1)

print(str(int(vlc_player.get_length()/1000)) + 's')

time.sleep(3)

#vlc_player.set_position(0.9995)

for i in range(0,50):
    v = 50 - i
    vlc_player.audio_set_volume(v)
    print(v, vlc_player.get_state(), vlc_player.get_position())
    time.sleep(0.1)

for i in range(0,50):
    v = i
    vlc_player.audio_set_volume(v)
    print(v, vlc_player.get_state(), vlc_player.get_position())
    time.sleep(0.1)

time.sleep(5)

vlc_player.stop()

time.sleep(3)
