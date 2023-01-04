#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2023 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------

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



def whisper_proc(model='large', inp_file='input.mp4', txt_file='temp.txt', srt_file='temp.srt', ):

    # ファイル確認、消去
    if (not os.path.exists(inp_file)):
        return False
    try:
        os.remove(txt_file) 
    except:
        pass
    try:
        os.remove(srt_file) 
    except:
        pass

    # 認識モデル
    print('Whisper認識設定 ' + model)
    whisper_model = whisper.load_model(model)

    # 音声認識
    print('Whisper音声認識')
    try:
        #result = whisper_model.transcribe(inp_file)
        result = whisper_model.transcribe(inp_file, verbose=True, )
        #result = whisper_model.transcribe(inp_file, verbose=True, task='translate')
    except:
        result = None

    if (result == None):
        print('★Whisper（処理）エラー')
        return False

    if (len(result['segments']) <= 0):
        print('★Whisper（認識０件）エラー')
        return False

    # ファイルオープン
    print('ファイル出力 ' + txt_file + ', ' + srt_file)
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
        st_str = st_str[:12]
        en = r['end']
        en_t = datetime.timedelta(seconds=en, )
        en_str = str(en_t).replace('.', ',')
        if (en_str[1:2] == ':'):
            en_str = '0' + en_str
        if (len(en_str) == 8):
            en_str = en_str + ',000000'
        en_str = en_str[:12]
        txt = r['text']
        #print(str(n), st_str, '-->', en_str, txt, )

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

    return True



def jimaku_proc(inp_file='input.mp4', srt_file='temp.srt', out_file='output.mp4', ):

    # ファイル確認、消去
    if (not os.path.exists(inp_file)):
        return False
    if (not os.path.exists(srt_file)):
        return False
    try:
        os.remove(out_file) 
    except:
        pass

    # 字幕合成
    print('字幕合成出力 ' + out_file)
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

    if (not os.path.exists(out_file)):
        return False

    return True



if __name__ == '__main__':

    # 'tiny','base','small','medium' or 'large'
    model = 'large'



    inp_file = 'temp3.mp4'
    txt_file = inp_file[:-4] + '_output.txt'
    srt_file = inp_file[:-4] + '_output.srt'
    out_file = inp_file[:-4] + '_output.mp4'

    res = whisper_proc(model, inp_file, txt_file, srt_file, )
    print(inp_file, res)
    if (res == True):
        ext = inp_file[-4:].lower()
        if (ext == '.mp4') or (ext == '.m4v'):
            res = jimaku_proc(inp_file, srt_file, out_file, )
            print(out_file, res)



    inp_file = 'temp4.m4v'
    txt_file = inp_file[:-4] + '_output.txt'
    srt_file = inp_file[:-4] + '_output.srt'
    out_file = inp_file[:-4] + '_output.mp4'

    res = whisper_proc(model, inp_file, txt_file, srt_file, )
    print(inp_file, res)
    if (res == True):
        ext = inp_file[-4:].lower()
        if (ext == '.mp4') or (ext == '.m4v'):
            res = jimaku_proc(inp_file, srt_file, out_file, )
            print(out_file, res)


