#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://aiacademy.jp/media/?p=3512

# pip install torch

# https://github.com/openai/whisper
# gitからzipダウンロード、解答後　↓
# cd C:\Users\admin\Documents\GitHub\py-etc\whisper\whisper-main
# python setup.py install


import whisper

model = whisper.load_model("tiny")
#model = whisper.load_model("base")
#model = whisper.load_model("small")
#model = whisper.load_model("medium")
#model = whisper.load_model("large")

result = model.transcribe("_sound_hallo.mp3")
print("result['text']")
print(result['text'])
print('')
print('result')
print(result)

#result = model.transcribe("_sound_hallo.mp3", verbose=True, task="translate")
#print(result["text"])



