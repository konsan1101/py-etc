#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import shutil
import os
import sys
import datetime

#ffmpeg -i test_input.mp4 -vf "select=gt(scene\,0.1), scale=640:360,showinfo" -vsync vfr %04d.jpg -f null - 2>test_output.txt
#ffmpeg -i test_input.mp4 -vf "select=gt(scene\,0.1), scale=640:360,showinfo" -vsync vfr "%03d.jpg"

if __name__ == '__main__':

    try:
        shutil.rmtree('temp')
    except:
        pass
    os.mkdir('temp')

    sfps   = 1
    scene = 0.1 #None
    #scene = None

    if (scene == None):
        ffmpeg = subprocess.Popen(['ffmpeg', '-i', 'test_input.flv', \
            '-filter:v', 'fps=fps=' + str(sfps) + ':round=down, showinfo', \
            'temp/%04d.jpg', \
            #], )
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
    else:
        ffmpeg = subprocess.Popen(['ffmpeg', '-i', 'test_input.flv', \
            #'-filter:v', 'fps=fps=' + str(sfps) + ':round=down, select=gt(scene\,' + str(scene) + '), scale=0:0, showinfo', \
            '-filter:v', 'select=gt(scene\,' + str(scene) + '), scale=0:0, showinfo', \
            '-vsync', 'vfr', 'temp/%04d.jpg', \
            #], )
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )
        
    logb, errb = ffmpeg.communicate()
    ffmpeg.terminate()
    ffmpeg = None

    #log = logb.decode()
    log = errb.decode()
    txts = log.split('\n')
    for txt in txts:
        #print(txt)

        if (txt.find('Parsed_showinfo')>0) and (txt.find('] n:')>0):
            # n, pts_time
            n = ''
            pts_time = ''
            x_n        = txt.find(' n:')
            x_pts      = txt.find(' pts:')
            x_pts_time = txt.find(' pts_time:')
            x_pos      = txt.find(' pos:')
            if (x_n != 0) and (x_pts != 0):
                n = txt[x_n+3:x_pts].strip()
            if (x_pts_time != 0) and (x_pos != 0):
                pts_time = txt[x_pts_time+10:x_pos].strip()

            if (n == '') or (pts_time == ''):
                #print(txt)
                pass
            else:
                #print(n,pts_time)

                # s => hhmmss
                dt1=datetime.datetime(1965,11,1,0,0,0,0)
                dt2=datetime.timedelta(seconds=float(pts_time))
                dtx=dt1+dt2
                stamp = dtx.strftime('%H%M%S.%f')
                #print(stamp[:-7])

                # rename
                seq4 = '{:04}'.format(int(n) + 1)
                f1 = 'temp/' + seq4 + '.jpg'
                f2 = 'temp/' + seq4 + '.' + stamp[:-3] + '.jpg'
                os.rename(f1, f2)

                print(f2)


