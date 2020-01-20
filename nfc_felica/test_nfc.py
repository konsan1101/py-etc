#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://www.bnote.net/raspberry_pi/felica_nfcpy.html

import nfc
import binascii

def connected(tag):
    idm = binascii.hexlify(tag.idm)
    print(idm)
    return False

clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})
clf.close()


