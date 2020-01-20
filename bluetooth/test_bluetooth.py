#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://teratail.com/questions/222946

import bluetooth
nearby_devices = bluetooth.discover_devices(lookup_names=True)
print("Found {} devices.".format(len(nearby_devices)))
for addr, name in nearby_devices:
    print(addr, name)


