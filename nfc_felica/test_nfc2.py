#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://nfcpy.readthedocs.io/en/latest/topics/get-started.html

import nfc
import binascii

def connected(tag):
    idm = binascii.hexlify(tag.idm)
    print(idm)
    return False

clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})
clf.close()


