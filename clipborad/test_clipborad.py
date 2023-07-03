#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://note.nkmk.me/python-pillow-imagegrab-grabclipboard/
# https://rightcode.co.jp/blog/information-technology/python-tesseract-image-processing-ocr
# https://github.com/UB-Mannheim/tesseract/wiki
# https://note.nkmk.me/python-pyperclip-usage/

import os
from PIL import ImageGrab, Image
import pyocr
import pyperclip
import time

#インストールしたTesseract-OCRのパスを環境変数「PATH」へ追記する。
#OS自体に設定してあれば以下の2行は不要
#path='C:\\Program Files\\Tesseract-OCR'
#os.environ['PATH'] = os.environ['PATH'] + path
 
#pyocrへ利用するOCRエンジンをTesseractに指定する。
tools = pyocr.get_available_tools()
print(tools)
print(tools[0].get_name())
tool = tools[0]

lastImage = ImageGrab.grabclipboard()
lastText  = pyperclip.paste()

while True:
    clipImage = ImageGrab.grabclipboard()
    if (clipImage != None):
        if (lastImage != clipImage):
            lastImage = clipImage    
            print('! cliped image.')
            #lastImage.show()

            #画像から文字を読み込む 3=完全自動ページ分割、ただしOSDなし。
            builder = pyocr.builders.TextBuilder(tesseract_layout=3)
            text = tool.image_to_string(lastImage, lang="jpn", builder=builder)
            print('OCR #' + text + '#')

    clipText = pyperclip.paste()
    if (clipText != ''):
        if (clipText != lastText):
            lastText = clipText
            print('! cliped text. #' + lastText + '#')

    time.sleep(1)




