#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pykakasi import kakasi

if (__name__ == '__main__'):

    # オブジェクトをインスタンス化
    kakasi = kakasi()
    # モードの設定：J(Kanji) to H(Hiragana)
    kakasi.setMode('J', 'H') 

    # 変換して出力
    conv = kakasi.getConverter()

    kanji = "形態素解析"
    kana  = conv.do(kanji)
    print(kana)

    kanji = "東京特許許可局"
    kana  = conv.do(kanji)
    print(kana)

    kanji = "近藤光男"
    kana  = conv.do(kanji)
    print(kana)

    kanji = "「今日はABCさん、宜しくお願いします。」"
    kana  = conv.do(kanji)
    print(kana)

    kanji = "己の役割を全うする、マインの友達"
    kana  = conv.do(kanji)
    print(kana)
