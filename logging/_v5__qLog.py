#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2020 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import sys
import datetime

import logging
from rainbow_logging_handler import RainbowLoggingHandler



class qLog_class:

    def __init__(self, filename='logfile', display=True, outfile=True, ):
        nowTime = datetime.datetime.now()
        self.filename = filename + '_' + nowTime.strftime('%Y%m%d.%H%M%S') + '.log'
        self.display  = display
        self.outfile  = outfile

        # ロガー定義
        self.logger_disp = logging.getLogger(filename + '_disp').getChild(__name__)
        self.logger_disp.setLevel(logging.DEBUG)
        self.logger_file = logging.getLogger(filename + '_file').getChild(__name__)
        self.logger_file.setLevel(logging.DEBUG)

        # コンソールハンドラー
        console_format  = logging.Formatter('%(asctime)s, %(message)s')
        console_handler = RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'yellow', True))
        console_handler.setFormatter(console_format)
        self.logger_disp.addHandler(console_handler)

        # ファイルハンドラー
        file_format  = logging.Formatter('%(asctime)s, %(lineno)d, %(levelname)s, %(message)s')
        file_handler = logging.FileHandler(self.filename, 'a')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_format)
        self.logger_file.addHandler(file_handler)

    def log(self, level='info', proc='', msg='info', display=None, outfile=None,):
        if (proc == ''):
            procname = proc
        else:
            procname = proc + ' : '

        if (display == None):
            display = self.display
        if (outfile == None):
            outfile = self.outfile

        if   (level=='info') or (level==logging.INFO):
            if (display == True):
                self.logger_disp.info(procname + msg)
            if (outfile == True):
                self.logger_file.info(procname + msg)
        elif (level=='debug') or (level==logging.DEBUG):
            if (display == True):
                self.logger_disp.debug(procname + msg)
            if (outfile == True):
                self.logger_file.debug(procname + msg)
        elif (level=='warning') or (level==logging.WARNING):
            if (display == True):
                self.logger_disp.warning(procname + msg)
            if (outfile == True):
                self.logger_file.warning(procname + msg)
        elif (level=='error') or (level==logging.ERROR):
            if (display == True):
                self.logger_disp.err(procname + msg)
            if (outfile == True):
                self.logger_file.err(procname + msg)
        elif (level=='critical') or (level==logging.CRITICAL):
            if (display == True):
                self.logger_disp.critical(procname + msg)
            if (outfile == True):
                self.logger_file.critical(procname + msg)
        else:
            self.logger_disp.critical(procname + msg)
            self.logger_file.critical(procname + msg)

    def exception(self, e):
            self.logger_disp.exception(e)
            self.logger_file.exception(e)



def sub():
    proc_name = 'sub'
    proc_id   = '{0:10s}'.format(proc_name).replace(' ', '_')

    qLog.log('info', proc_id, u'start')
    qLog.log('info', proc_id, u'error test ↓')
    try:
        a=a/0
    except Exception as e:
        qLog.exception(e)        
    qLog.log('info', proc_id, u'end')
    
    return True



if __name__ == '__main__':
    qLog = qLog_class()

    main_name = 'main'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')
    qLog.log('info', main_id, u'run')

    x = sub()


