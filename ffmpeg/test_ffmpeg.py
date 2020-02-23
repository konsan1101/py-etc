#!/usr/bin/env python
# -*- coding: utf-8 -*-

#pip install python-ffmpeg

import os
import time
import ffmpeg

# 入力
# -f gdigrab -i desktop
#stream = ffmpeg.input('-f gdigrab -i desktop')
#stream = ffmpeg.input('gdigrab')
stream = ffmpeg.input('test_input.flv')

# 出力
os.remove('test_output.mp4')
stream = ffmpeg.output(stream, 'test_output.mp4',t=2,ss=2)

#stream = ffmpeg.drawbox(stream,0,0,320,240,0)

# 実行
#ffmpeg.run(stream)
ffmpeg.run_async(stream)


time.sleep(10)

