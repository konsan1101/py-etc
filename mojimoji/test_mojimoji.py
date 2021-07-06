#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mojimoji
import unicodedata



def in_japanese(txt=''):
        t = txt.replace('\r', '')
        t = t.replace('\n', '')
        try:
            for s in t:
                name = unicodedata.name(s) 
                print(name)
                if ('CJK UNIFIED' in name) \
                or ('HIRAGANA' in name) \
                or ('KATAKANA' in name):
                    return True
        except Exception as e:
            pass
        return False



if __name__ == '__main__':


    txts = [u'早く', u'こんにちは',u'ｺﾝﾆﾁﾜ', ]

    maxlen = 0
    for i in range(0, len(txts)):
        if (in_japanese(txts[i]) == True):
            lenstr = len(txts[i]) * 2
        else:
            lenstr = len(txts[i])
        if (maxlen < lenstr):
            maxlen = lenstr

    print(maxlen)

    for i in range(0, len(txts)):
        zenkaku = mojimoji.han_to_zen(txts[i])
        print(zenkaku)


