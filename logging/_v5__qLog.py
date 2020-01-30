#!/usr/bin/env python
# -*- coding: utf-8 -*-

# COPYRIGHT (C) 2014-2020 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.



import sys
import os
import time
import datetime
import codecs



import logging
from rainbow_logging_handler import RainbowLoggingHandler



class qLog_class:

    def __init__(self, ):
        self.mode     = 'nologger' 
        self.logfile  = ''
        self.display  = True
        self.outfile  = False

    def init(self, mode='nologger', filename='', display=True, outfile=True, ):
        self.mode     = mode
        if (filename == ''):
            if (not os.path.isdir('temp')):
                os.makedirs('temp')
            if (not os.path.isdir('temp/_log')):
                os.makedirs('temp/_log')
            filename = 'temp/_log/' + os.path.basename(__file__)
        nowTime = datetime.datetime.now()
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
            file_handler = logging.FileHandler(self.logfile, 'a', 'utf-8', )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_format)
            self.logger_file.addHandler(file_handler)

    def log(self, level='info', proc='', msg='info', display=None, outfile=None,):
        if (proc == ''):
            procname = ''
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
                if   (level=='info') or (level==logging.INFO):
                    print( txt )
                elif (level=='debug') or (level==logging.DEBUG):
                    print( self.colorTxt(txt=txt, fgColor='cyan', fgLine='', bgColor='', ) )
                elif (level=='warning') or (level==logging.WARNING):
                    print( self.colorTxt(txt=txt, fgColor='yellow', fgLine='', bgColor='', ) )
                elif (level=='error') or (level==logging.ERROR):
                    print( self.colorTxt(txt=txt, fgColor='red', fgLine='', bgColor='', ) )
                elif (level=='critical') or (level==logging.CRITICAL):
                    print( self.colorTxt(txt=txt, fgColor='white', fgLine='', bgColor='red', ) )
                else:
                    print( self.colorTxt(txt=txt, fgColor='white', fgLine='', bgColor='red', ) )
            if (outfile == True):
                try:
                    nowTime = datetime.datetime.now()
                    s  = nowTime.strftime('%Y-%m-%d %H:%M:%S, ')
                    s += str(level) + ', '
                    s += str(txt)
                    w = codecs.open(self.logfile, 'a', 'utf-8')
                    w.write(s + '\n')
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
            self.log(level='error', proc='', msg=txt, )

    def colorTxt(self, txt='', fgColor='', fgLine='', bgColor='', ):
        txtColor = ''
        if   (fgLine != ''):
            txtColor += '\033[4m'
        if   (fgColor == 'black'):
            txtColor += '\033[30m'
        elif (fgColor == 'red'):
            txtColor += '\033[31m'
        elif (fgColor == 'green'):
            txtColor += '\033[32m'
        elif (fgColor == 'yellow'):
            txtColor += '\033[33m'
        elif (fgColor == 'blue'):
            txtColor += '\033[34m'
        elif (fgColor == 'magenta'):
            txtColor += '\033[35m'
        elif (fgColor == 'cyan'):
            txtColor += '\033[36m'
        elif (fgColor == 'white'):
            txtColor += '\033[37m'
        if   (bgColor == 'black'):
            txtColor += '\033[40m'
        elif (bgColor == 'red'):
            txtColor += '\033[41m'
        elif (bgColor == 'green'):
            txtColor += '\033[42m'
        elif (bgColor == 'yellow'):
            txtColor += '\033[43m'
        elif (bgColor == 'blue'):
            txtColor += '\033[44m'
        elif (bgColor == 'magenta'):
            txtColor += '\033[45m'
        elif (bgColor == 'cyan'):
            txtColor += '\033[46m'
        elif (bgColor == 'white'):
            txtColor += '\033[47m'
        resetColor = ''
        if (txtColor != ''):
            resetColor = '\033[0m'
        return txtColor + str(txt) + resetColor



def sub():
    proc_name = 'sub'
    proc_id   = '{0:10s}'.format(proc_name).replace(' ', '_')

    qLog.log('info', proc_id, 'start')
    qLog.log('info', proc_id, 'error test ↓')
    try:
        a=100/0
    except Exception as e:
        qLog.exception(e)        
    qLog.log('info', proc_id, 'end')
    
    return True



if __name__ == '__main__':
    qLog = qLog_class()
    qLog.init(mode='nologger', filename='', )

    main_name = 'main'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')
    qLog.log('info', main_id, 'run')

    qLog.log('info'    , main_id, '')
    qLog.log('debug'   , main_id, 'debug')
    qLog.log('warning' , main_id, 'warning')
    qLog.log('error'   , main_id, 'error')
    qLog.log('critical', main_id, 'critical')
    qLog.log('info'    , main_id, '')

    x = sub()


