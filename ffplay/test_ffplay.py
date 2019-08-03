#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == '__main__':

    ffplay = subprocess.Popen(['ffmpeg', '-i', 'test_input.flv', \
        '-vf', 'select=gt(scene\,0.1), scale=0:0,showinfo', \
        '-vsync', 'vfr', 'temp/%04d.jpg', \
        #], )
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

    ffplay.terminate()
    ffplay = None


