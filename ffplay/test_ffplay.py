#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess

if __name__ == '__main__':

    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -fs
    #ffplay -i test_input.flv -volume 100 -window_title "test_input.flv" -noborder -autoexit -x 320 -y 240

    ffplay = subprocess.Popen(['ffplay', '-i', 'test_input.flv', \
                                '-volume', '100', \
                                '-window_title', 'test_input.flv', \
                                '-noborder', '-autoexit', \
                                '-x', '320', '-y', '240', \
        #], )
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

    ffplay.terminate()
    ffplay = None


