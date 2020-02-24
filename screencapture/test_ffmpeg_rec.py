#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import signal
import time

filename = 'desktop.mp4'
if (os.path.isfile(filename)):
    os.remove(filename)
ffmpeg = subprocess.Popen(['ffmpeg', '-f', 'gdigrab', '-i', 'desktop', '-r', '5', filename, ],
                           stdin=subprocess.PIPE, )

time.sleep(10.00)

ffmpeg.stdin.write(b'q\n')
ffmpeg.stdin.flush()
ffmpeg.wait()
ffmpeg.terminate()
ffmpeg = None


