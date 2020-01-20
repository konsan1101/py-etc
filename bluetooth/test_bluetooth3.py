#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://va009039.blogspot.com/2011/01/pythonbluetooth.html

import bluetooth # PyBluez
import time
import datetime

old_devices = set()
while True:
    try:
        nearby_devices = bluetooth.discover_devices(lookup_names = True)
    except:
        print('err')
        time.sleep(10)
    else:
        dt = datetime.datetime.now()
        dt_str = dt.strftime("%Y/%m/%d %H:%M:%S")
        new_devices = set(nearby_devices)
        for addr,name in new_devices-old_devices:
            print( u"+ %s %s %s" % (dt_str, addr, name.decode('utf-8')) )
        for addr,name in old_devices-new_devices:
            print( u"- %s %s %s" % (dt_str, addr, name.decode('utf-8')) )
        old_devices = new_devices.copy()
        time.sleep(3)


