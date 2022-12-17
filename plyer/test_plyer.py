#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

#import plyer
from plyer import utils; platform = utils.platform
from plyer import notification

def bannerMSG(title='Message', txt='', ):
        if (txt == ''):
            return False

        #plyer.notification.notify(
        notification.notify(
                title=title,
                message=txt,
                timeout=10, 
                app_name='python', 
                app_icon='_icons/RiKi_start.ico', 
                ticker='', 
                toast=False)

if __name__ == '__main__':

    time.sleep(10)
    bannerMSG(title='Message', txt='テスト1', )
    time.sleep(2)
    bannerMSG(title='Message', txt='テスト2', )
    time.sleep(20)


