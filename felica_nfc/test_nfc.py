#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://www.bnote.net/raspberry_pi/felica_nfcpy.html
# https://qiita.com/bussorenre/items/48af677c6778c6597f60

import nfc
import binascii

def connected(tag):
    idm = binascii.hexlify(tag.idm)
    print(idm)
    return False

clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})
clf.close()


