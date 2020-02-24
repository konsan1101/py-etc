#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess
import signal
import time

filename = 'camera.mp4'
if (os.path.isfile(filename)):
    os.remove(filename)
ffmpeg = subprocess.Popen(['ffmpeg', '-f', 'dshow', '-i', "video=Microsoft Camera Front", '-r', '5', 'camera.mp4', ],
                           stdin=subprocess.PIPE, )

time.sleep(10.00)

ffmpeg.stdin.write(b'q\n')
ffmpeg.stdin.flush()
ffmpeg.wait()
ffmpeg.terminate()
ffmpeg = None


