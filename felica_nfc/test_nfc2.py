#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://tech-blog.cloud-config.jp/2019-04-27-new-hire-training-windows-nfcpy/

import nfc
import binascii

clf = nfc.ContactlessFrontend('usb')
print('touch card:')
try:
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})
finally:
    clf.close()
idm = binascii.hexlify(tag.idm)
print(idm)
print('please released card')


