#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://dev.classmethod.jp/articles/python-crypto-libraries/

# pip install pycryptodome

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

if __name__ == '__main__':

    key = get_random_bytes(16)
    print(key)

    data = b'Hoge Hoge'
    print(data)

    aes_mode = AES.MODE_EAX
    #aes_mode = AES.MODE_CCM
    #aes_mode = AES.MODE_GCM

    cipher_enc = AES.new(key, aes_mode)
    crypto_bin = cipher_enc.encrypt(data)

    print(crypto_bin)
    crypto_text = base64.b64encode(crypto_bin)
    print(crypto_text)

    crypto_bin = base64.b64decode(crypto_text)
    print(crypto_bin)

    cipher_dec = AES.new(key, aes_mode, cipher_enc.nonce)
    data = cipher_dec.decrypt(crypto_bin)
    print(data)


