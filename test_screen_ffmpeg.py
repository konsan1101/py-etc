#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import signal
import time

ffmpeg = subprocess.Popen(['ffmpeg', '-f', 'gdigrab', '-i', 'desktop', '-r', '5', 'desktop.mp4', ])
time.sleep(10.00)
ffmpeg.send_signal(signal.CTRL_C_EVENT)
ffmpeg.terminate(10.00)
ffmpeg = None

