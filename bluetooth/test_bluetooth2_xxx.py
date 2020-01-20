#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://qiita.com/dz_/items/4e858e4d50db19b57491

from bluetooth.ble import DiscoveryService

service = DiscoveryService()
devices = service.discover(2)

for address, name in devices.items():
    print("name: {}, address: {}".format(name, address))


