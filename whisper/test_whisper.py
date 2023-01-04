#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ★　メモ 2023/01/04時点
#   pytorchはPython3.10以下でしか実行できない。torchの更新待ち。
#   またexe化も出来ない。原因不明。

# ★　以下、実行環境構築法
#   https://github.com/openai/whisper
#   gitからzipダウンロード、解凍後、以下を実行する。↓
#   cd C:\Users\admin\Documents\GitHub\py-etc\whisper\whisper-main
#   python setup.py install

# 以下、不要。
#   pip install torch
#   pip install whisper



import sys
import os
import time
import datetime
import codecs
import glob

import subprocess

import whisper



file_name = 'temp3.mp4'
#file_name = 'temp4.m4v'
inp_file = file_name
txt_file = file_name[:-4] + '_output.txt'
srt_file = file_name[:-4] + '_output.srt'
out_file = file_name[:-4] + '_output.mp4'

try:
    os.remove(txt_file) 
except:
    pass
try:
    os.remove(srt_file) 
except:
    pass
try:
    os.remove(out_file) 
except:
    pass



# 認識モデル
#model = whisper.load_model('tiny')
#model = whisper.load_model('base')
#model = whisper.load_model('small')
#model = whisper.load_model('medium')
model = whisper.load_model('large')

# 音声認識
#result = model.transcribe(file_name, verbose=True, task='translate')
#result = model.transcribe(file_name)
try:
    result = model.transcribe(file_name, verbose=True, )
except:
    result = None

if (result == None):
    print('★Whisper（処理）エラー')
else:
    if (len(result['segments']) <= 0):
        print('★Whisper（認識０件）エラー')
    else:

        # ファイルオープン
        txtf = codecs.open(txt_file, mode='w', encoding='utf-8', )
        srtf = codecs.open(srt_file, mode='w', encoding='utf-8', )

        # ファイル出力
        n = 0
        for r in result['segments']:
            n += 1
            st = r['start']
            st_t = datetime.timedelta(seconds=st, )
            st_str = str(st_t).replace('.', ',')
            if (st_str[1:2] == ':'):
                st_str = '0' + st_str
            if (len(st_str) == 8):
                st_str = st_str + ',000000'
            en = r['end']
            en_t = datetime.timedelta(seconds=en, )
            en_str = str(en_t).replace('.', ',')
            if (en_str[1:2] == ':'):
                en_str = '0' + en_str
            if (len(en_str) == 8):
                en_str = en_str + ',000000'
            txt = r['text']
            print(str(n), st_str, '-->', en_str, txt, )

            # テキスト
            txtf.write(str(txt) + '\n')

            # 字幕
            srtf.write(str(n) + '\n')
            srtf.write(st_str + ' --> ' + en_str + '\n')
            srtf.write(str(txt) + '\n')
            srtf.write('\n')

        # ファイルクローズ
        txtf.close()
        txtf = None
        srtf.close()
        srtf = None

        # 字幕合成
        ffmpeg = subprocess.Popen(['ffmpeg',
            '-i', inp_file,
            '-i', srt_file,
            '-c', 'copy', '-c:s', 'mov_text', '-metadata:s:s:0', 'language=jpn',
            out_file,
            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        # 時限待機
        if (not ffmpeg is None):
            checkTime = time.time()
            while ((time.time() - checkTime) < 30):
                line = ffmpeg.stderr.readline()
                #if (len(line) != 0):
                #    print(line.decode())
                if (not line) and (not ffmpeg.poll() is None):
                    break
                time.sleep(0.01)
        ffmpeg.terminate()
        ffmpeg = None


