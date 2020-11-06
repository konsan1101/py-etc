#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://sehermitage.web.fc2.com/crypto/python_crypt.html

# pip install pycryptodome

import Crypto.Cipher.AES as AES
import Crypto.Util.Padding as PAD
import base64

if __name__ == '__main__':

    #key = b'Testxtestx01'
    key = base64.b64encode(b'Testxtestx01')

    ptext = 'test'

    iv = b'0' * 16
    aes = AES.new(key, AES.MODE_CBC, iv)
    data1 = PAD.pad(ptext.encode('utf-8'), 16, 'pkcs7')
    cipher = aes.encrypt(data1)

    cipher_text = base64.b64encode(cipher)
    print(cipher_text)

    aes = AES.new(key, AES.MODE_CBC, iv)
    data2 = aes.decrypt(cipher)
    plain = PAD.unpad(data2, 16, 'pkcs7')
    print(plain.decode('ascii'))


    