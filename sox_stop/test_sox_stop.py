#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 20200223 結論　いろいろやったけど、terminate命令で止めるのが無難。

import time
import subprocess
import signal

sox = subprocess.Popen(['sox', '-d', 'test.wav'], stdin=subprocess.PIPE, )

time.sleep(5.00)

print('stop start')

#sox.send_signal(signal.SIGINT)
#sox.send_signal(signal.CTRL_C_EVENT)
#sox.stdin.write(b'^C')
#sox.stdin.flush()

print('wait 5s')
time.sleep(5.00)

sox.terminate()
sox = None


