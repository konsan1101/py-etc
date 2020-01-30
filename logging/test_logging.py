#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://qiita.com/__init__/items/91e5841ed53d55a7895e
# https://github.com/laysakura/rainbow_logging_handler

import sys
import logging
from rainbow_logging_handler import RainbowLoggingHandler



def test():
    logger.info('info child')



if __name__ == '__main__':

    # ログ処理
    logger = logging.getLogger('main').getChild(__name__)
    logger.setLevel(logging.DEBUG)

    # setup `RainbowLoggingHandler`
    console_format  = logging.Formatter('[%(funcName)s], [%(levelname)s], [%(message)s]')
    console_handler = RainbowLoggingHandler(sys.stderr, color_funcName=('black', 'yellow', True))
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    file_format  = logging.Formatter('[%(asctime)s], [%(lineno)d], [%(name)s], [%(funcName)s], [%(levelname)s], [%(message)s]')
    file_handler = logging.FileHandler('logfile.log', 'a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)

    logger.critical('critical')
    logger.error('error')
    logger.warning('warning')
    logger.info('info')
    logger.debug('debug')
    try:
        a = 1 / 0
    except Exception as e:
        logger.exception(e)        
    logger.info('info')
    
    test()


