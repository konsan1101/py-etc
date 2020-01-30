#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime

import _v5__qLog



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
    qLog = _v5__qLog.qLog_class('test')

    main_name = 'main'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')
    qLog.log('info', main_id, u'run')

    x = sub()


