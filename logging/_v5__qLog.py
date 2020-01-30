#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2020 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import os
import sys
import datetime
import codecs

import logging
from rainbow_logging_handler import RainbowLoggingHandler



class qLog_class:

    def __init__(self, mode='logger', filename='', display=True, outfile=True, ):
        nowTime = datetime.datetime.now()
        self.mode     = mode
        if (filename == ''):
            if (not os.path.isdir('temp')):
                os.makedirs('temp')
            if (not os.path.isdir('temp/_log')):
                os.makedirs('temp/_log')
            filename = 'temp/_log/' + os.path.basename(__file__)
        self.logfile  = filename + '_' + nowTime.strftime('%Y%m%d.%H%M%S') + '.log'
        self.display  = display
        self.outfile  = outfile

        # ロガー定義
        if (self.mode == 'logger'):
            self.logger_disp = logging.getLogger('disp')
            self.logger_disp.setLevel(logging.DEBUG)
            self.logger_file = logging.getLogger('file')
            self.logger_file.setLevel(logging.DEBUG)

        # コンソールハンドラー
        if (self.mode == 'logger'):
            console_format  = logging.Formatter('%(asctime)s, %(message)s')
            console_handler = RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'yellow', True))
            console_handler.setFormatter(console_format)
            self.logger_disp.addHandler(console_handler)

        # ファイルハンドラー
        if (self.mode == 'logger'):
            file_format  = logging.Formatter('%(asctime)s, %(lineno)d, %(levelname)s, %(message)s')
            file_handler = logging.FileHandler(self.logfile, 'a')
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

        # ログ出力（logger）
        txt = str(procname + msg)
        if (self.mode == 'logger'):
            if   (level=='info') or (level==logging.INFO):
                if (display == True):
                    self.logger_disp.info(txt)
                if (outfile == True):
                    self.logger_file.info(txt)
            elif (level=='debug') or (level==logging.DEBUG):
                if (display == True):
                    self.logger_disp.debug(txt)
                if (outfile == True):
                    self.logger_file.debug(txt)
            elif (level=='warning') or (level==logging.WARNING):
                if (display == True):
                    self.logger_disp.warning(txt)
                if (outfile == True):
                    self.logger_file.warning(txt)
            elif (level=='error') or (level==logging.ERROR):
                if (display == True):
                    self.logger_disp.error(txt)
                if (outfile == True):
                    self.logger_file.error(txt)
            elif (level=='critical') or (level==logging.CRITICAL):
                if (display == True):
                    self.logger_disp.critical(txt)
                if (outfile == True):
                    self.logger_file.critical(txt)
            else:
                self.logger_disp.critical(txt)
                self.logger_file.critical(txt)

        # ログ出力（local）
        else:
            txt = str(procname + msg)
            if (display == True):
                print(txt)
            if (outfile == True):
                try:
                    w = codecs.open(self.logfile, 'a', 'utf-8')
                    w.write(str(txt) + '\n')
                    w.close()
                    w = None
                except:
                    pass
            
    def exception(self, e):
        # ログ出力（logger）
        txt = str(e.args)
        if (self.mode == 'logger'):
            self.logger_disp.exception(txt)
            self.logger_file.exception(txt)
        else:
            print(txt)
            try:
                w = codecs.open(self.logfile, 'a', 'utf-8')
                w.write(str(txt) + '\n')
                w.close()
                w = None
            except:
                pass



def sub():
    proc_name = 'sub'
    proc_id   = '{0:10s}'.format(proc_name).replace(' ', '_')

    qLog.log('info', proc_id, u'start')
    qLog.log('info', proc_id, u'error test ↓')
    try:
        a=100/0
    except Exception as e:
        qLog.exception(e)        
    qLog.log('info', proc_id, u'end')
    
    return True



if __name__ == '__main__':
    qLog = qLog_class(mode='logger', filename='', )
    #qLog = qLog_class(mode='nologger', filename='', )

    main_name = 'main'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')
    qLog.log('info', main_id, u'run')

    x = sub()


