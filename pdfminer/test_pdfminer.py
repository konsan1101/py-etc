#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://freeheroblog.com/pdfminer/

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

fp = open('test.pdf', 'rb')

# 出力する
outfp = StringIO()

# PDFファイル内のリソース(テキスト、画像、罫線など)を管理する総元締め的なクラス
rmgr = PDFResourceManager()
# PDFファイルのレイアウトパラメータを保持するクラス
lprms = LAParams()
# PDFファイル内のテキストを取り出す機能を提供するクラス 
device = TextConverter(rmgr, outfp, laparams=lprms)
# PDFファイルを1ページずつ取得。集合(set)として保持するクラス
iprtr = PDFPageInterpreter(rmgr, device)


for page in PDFPage.get_pages(fp):
    iprtr.process_page(page)

text = outfp.getvalue()

outfp.close()
device.close()
fp.close()
print(text)