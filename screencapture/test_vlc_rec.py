#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import signal
import time

vlc = subprocess.Popen(['vlc', 'screen://', ':screen-fps=5', ':live-caching=300', \
    '--sout=#transcode{vcodec=h264,acodec=none}:standard{access=file,mux=mp4,dst="desktop.mp4"}', \
    '--qt-start-minimized', ])

time.sleep(10.00)

vlcx = subprocess.Popen(['vlc', 'vlc://quit', ])

vlc = None


