#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time
import os

nowTime1 = datetime.datetime.now()
stamp1   = nowTime1.strftime('%Y%m%d.%H%M%S')
print('datetime:', stamp1)

nowStamp = time.time()
nowTime2 = datetime.datetime.fromtimestamp(nowStamp)
stamp2   = nowTime2.strftime('%Y%m%d.%H%M%S')
print('time:', stamp2)

fileStamp = os.path.getmtime('input.png')
#fileStamp = os.path.getmtime('test_getfiletime.py')
fileTime  = datetime.datetime.fromtimestamp(fileStamp)
stamp3    = fileTime.strftime('%Y%m%d.%H%M%S')
print('file:', stamp3)


