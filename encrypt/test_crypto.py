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

    cipher_enc = AES.new(key, AES.MODE_EAX)
    crypto_bin, tag = cipher_enc.encrypt_and_digest(data)

    print(crypto_bin)
    crypto_text = base64.b64encode(crypto_bin)
    print(crypto_text)

    crypto_bin = base64.b64decode(crypto_text)
    print(crypto_bin)

    cipher_dec = AES.new(key, AES.MODE_EAX, cipher_enc.nonce)
    data = cipher_dec.decrypt_and_verify(crypto_bin, tag)
    print(data)


