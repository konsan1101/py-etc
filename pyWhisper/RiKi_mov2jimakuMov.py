#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2023 Mitsuo KONDOU.
# This software is released under the MIT License.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------

# ★　以下、実行環境構築法
## 　↓　2023/06/25操作不要
##   https://github.com/openai/whisper
##   gitからzipダウンロード、解凍後、以下を実行する。↓
##   cd C:\Users\admin\Documents\GitHub\py-etc\whisper\whisper-main
##   python setup.py install
## 　↑　2023/06/25操作不要
#
#    python -m pip  install --upgrade screeninfo
#    python -m pip  install --upgrade pyautogui
#    python -m pip  install --upgrade pywin32
#    python -m pip  install --upgrade psutil
#    python -m pip  install --upgrade rainbow-logging-handler
#    python -m pip  install --upgrade pycryptodome
#
#    python -m pip  install --upgrade torch
#    python -m pip  install --upgrade openai-whisper
#
#    python -m pip  install --upgrade six
#    python -m pip  install --upgrade tqdm
#    python -m pip  install --upgrade packaging
#    python -m pip  install --upgrade tokenizers

# ★　CUDA有効化
#   pip uninstall torch
#   pip install   torch  --extra-index-url https://download.pytorch.org/whl/cu116

# ★　メモ 2023/06/25時点
#   exe化可能。
#    pyinstaller %pyname%.py  -F --log-level ERROR  --copy-metadata tokenizers --copy-metadata packaging --copy-metadata tqdm --copy-metadata regex --copy-metadata requests --copy-metadata packaging --copy-metadata filelock --copy-metadata numpy --copy-metadata tokenizers --collect-data whisper



import sys
import os
import time
import datetime
import codecs
import glob

import subprocess

import torch
import whisper



# 共通ルーチン
import   _v6__qFunc
qFunc  = _v6__qFunc.qFunc_class()
import   _v6__qLog
qLog   = _v6__qLog.qLog_class()



qPath_temp  = 'temp/'
qPath_log   = 'temp/_log/'



class qWhisper_class:

    def __init__(self, runMode='debug', cuda=False, model='large-v2', ): 

        # CUDA 無効化（有効な場合、GPUメモリが大量に必要！）
        print('torch version        =', torch.__version__)
        print('torch cuda available =', torch.cuda.is_available())
        if (cuda == False) and (torch.cuda.is_available() == True):
            print('torch.cuda.無効化！')
            torch.cuda.is_available = lambda: False
            print('torch cuda available =', torch.cuda.is_available())

        # Whisper認識設定
        #print('Whisper認識設定 ' + model)
        if (not os.path.exists('_whisper_model/' + str(model) + '.pt')):
            self.whisper_model = whisper.load_model(model)
        else:
            self.whisper_model = whisper.load_model(model, download_root='_whisper_model')



    def whisper_proc(self, inp_file='input.mp4', wav_file='temp.wav', txt_file='temp.txt', srt_file='temp.srt', ):

        # ファイル確認、消去
        if (not os.path.exists(inp_file)):
            return False
        try:
            os.remove(wav_file) 
        except:
            pass
        try:
            os.remove(txt_file) 
        except:
            pass
        try:
            os.remove(srt_file) 
        except:
            pass

        # 音声分離
        #print('音声分離出力 ' + wav_file)
        ffmpeg = subprocess.Popen(['ffmpeg', '-y',
            '-i', inp_file,
            '-af', 'dynaudnorm', 
            '-ar', '16000', '-ac', '1', 
            wav_file,
            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        # 時限待機
        if (ffmpeg is not None):
            checkTime = time.time()
            while ((time.time() - checkTime) < 30):
                line = ffmpeg.stderr.readline()
                #if (len(line) != 0):
                #    print(line.decode())
                if (not line) and (ffmpeg.poll() is not None):
                    break
                time.sleep(0.01)
        ffmpeg.terminate()
        ffmpeg = None

        # 音声認識
        #print('Whisper音声認識')
        try:
            #result = whisper_model.transcribe(inp_file)
            result = self.whisper_model.transcribe(wav_file, verbose=True, fp16=False, )
            #result = whisper_model.transcribe(inp_file, verbose=True, task='translate')
        except:
            result = None

        if (result is None):
            print('★Whisper（処理）エラー')
            return False

        if (len(result['segments']) <= 0):
            print('★Whisper（認識０件）エラー')
            return False

        # ファイルオープン
        #print('ファイル出力 ' + txt_file + ', ' + srt_file)
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



    def jimaku_proc(self, inp_file='input.mp4', srt_file='temp.srt', out_file='output.mp4', ):

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
        #print('字幕合成出力 ' + out_file)
        ffmpeg = subprocess.Popen(['ffmpeg', '-y',
            '-i', inp_file,
            '-i', srt_file,
            '-c', 'copy', '-c:s', 'mov_text', '-metadata:s:s:0', 'language=jpn',
            out_file,
            ], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, )

        # 時限待機
        if (ffmpeg is not None):
            checkTime = time.time()
            while ((time.time() - checkTime) < 30):
                line = ffmpeg.stderr.readline()
                #if (len(line) != 0):
                #    print(line.decode())
                if (not line) and (ffmpeg.poll() is not None):
                    break
                time.sleep(0.01)
        ffmpeg.terminate()
        ffmpeg = None

        if (not os.path.exists(out_file)):
            return False

        return True



# シグナル処理
import signal
def signal_handler(signal_number, stack_frame):
    print(os.path.basename(__file__), 'accept signal =', signal_number)

#signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGINT,  signal.SIG_IGN)
signal.signal(signal.SIGTERM, signal.SIG_IGN)



runMode = 'debug'

# 'tiny','base','small','medium','large-v2'
#model   = 'tiny'
model   = 'base'
#model   = 'small'
#model   = 'medium'
#model   = 'large-v2'

inpFile = ''



if __name__ == '__main__':
    main_name = 'whisper'
    main_id   = '{0:10s}'.format(main_name).replace(' ', '_')

    #　実行パスセット
    path_current = os.path.dirname(sys.argv[0])
    #print(path_current)
    os.chdir(path_current)

    # ディレクトリ作成
    qFunc.makeDirs(qPath_temp, remove=False, )
    qFunc.makeDirs(qPath_log,  remove=False, )

    # ログ
    nowTime  = datetime.datetime.now()
    filename = qPath_log + nowTime.strftime('%Y%m%d.%H%M%S') + '.' + os.path.basename(__file__) + '.log'
    qLog.init(mode='logger', filename=filename, )
    qLog.log('info', main_id, 'init')
    qLog.log('info', main_id, 'exsample.py runMode, ')

    # パラメータ
    if (True):
        if (len(sys.argv) >= 2):
            p = str(sys.argv[1])
            if (os.path.exists(p)):
                inpFile = p
                model   = 'large-v2'
            else:
                runMode = p.lower()
        if (len(sys.argv) >= 3):
            model = str(sys.argv[2])
        if (len(sys.argv) >= 4):
            inpFile = str(sys.argv[3])

        qLog.log('info', main_id, 'runMode = ' + str(runMode ))
        qLog.log('info', main_id, 'model   = ' + str(model   ))
        qLog.log('info', main_id, 'inpFile = ' + str(inpFile ))

    # 設定
    if (True):
        qWhisper = qWhisper_class(cuda=False, model=model, )

    # 処理開始
    if (True):
        start_now  = datetime.datetime.now()
        start_time = start_now.strftime('%Y/%m/%d %H:%M:%S')

        qLog.log('info', main_id, 'start')

    # debug 1
    if (runMode == 'debug') and (inpFile == ''):

        inp_file = 'temp_0104/temp3.mp4'
        wav_file = inp_file[:-4] + '_output.wav'
        txt_file = inp_file[:-4] + '_output.txt'
        srt_file = inp_file[:-4] + '_output.srt'
        out_file = inp_file[:-4] + '_output.mp4'

        qLog.log('info', main_id, '音声認識 (Whisper)')
        qLog.log('info', main_id, 'input = ' + inp_file)
        res = qWhisper.whisper_proc(inp_file, wav_file, txt_file, srt_file, )
        #print(inp_file, res)
        qLog.log('info', main_id, 'result= ' + str(res))
        if (os.path.exists(wav_file)):
            qLog.log('info', main_id, 'wav   = ' + wav_file)
        if (os.path.exists(txt_file)):
            qLog.log('info', main_id, 'txt   = ' + txt_file)
        if (os.path.exists(srt_file)):
            qLog.log('info', main_id, 'srt   = ' + srt_file)
        if (res == True):
            ext = inp_file[-4:].lower()
            if (ext == '.mp4') or (ext == '.m4v'):
                qLog.log('info', main_id, '字幕合成')
                res = qWhisper.jimaku_proc(inp_file, srt_file, out_file, )
                #print(out_file, res)
                qLog.log('info', main_id, 'jimaku=' + str(res))
                if (os.path.exists(out_file)):
                    qLog.log('info', main_id, 'output= ' + out_file)

    # debug 2
    if (runMode == 'debug') and (inpFile == ''):

        inp_file = 'temp_pfm/temp4.m4v'
        wav_file = inp_file[:-4] + '_output.wav'
        txt_file = inp_file[:-4] + '_output.txt'
        srt_file = inp_file[:-4] + '_output.srt'
        out_file = inp_file[:-4] + '_output.mp4'

        qLog.log('info', main_id, '音声認識 (Whisper)')
        qLog.log('info', main_id, 'input = ' + inp_file)
        res = qWhisper.whisper_proc(inp_file, wav_file, txt_file, srt_file, )
        #print(inp_file, res)
        qLog.log('info', main_id, 'result= ' + str(res))
        if (os.path.exists(wav_file)):
            qLog.log('info', main_id, 'wav   = ' + wav_file)
        if (os.path.exists(txt_file)):
            qLog.log('info', main_id, 'txt   = ' + txt_file)
        if (os.path.exists(srt_file)):
            qLog.log('info', main_id, 'srt   = ' + srt_file)
        if (res == True):
            ext = inp_file[-4:].lower()
            if (ext == '.mp4') or (ext == '.m4v'):
                qLog.log('info', main_id, '字幕合成')
                res = qWhisper.jimaku_proc(inp_file, srt_file, out_file, )
                #print(out_file, res)
                qLog.log('info', main_id, 'jimaku=' + str(res))
                if (os.path.exists(out_file)):
                    qLog.log('info', main_id, 'output= ' + out_file)



    # 処理実行
    if (inpFile != ''):

        inp_file = inpFile
        wav_file = inp_file[:-4] + '_output.wav'
        txt_file = inp_file[:-4] + '_output.txt'
        srt_file = inp_file[:-4] + '_output.srt'
        out_file = inp_file[:-4] + '_output.mp4'

        qLog.log('info', main_id, '音声認識 (Whisper)')
        qLog.log('info', main_id, 'input = ' + inp_file)
        res = qWhisper.whisper_proc(inp_file, wav_file, txt_file, srt_file, )
        #print(inp_file, res)
        qLog.log('info', main_id, 'result= ' + str(res))
        if (os.path.exists(wav_file)):
            qLog.log('info', main_id, 'wav   = ' + wav_file)
        if (os.path.exists(txt_file)):
            qLog.log('info', main_id, 'txt   = ' + txt_file)
        if (os.path.exists(srt_file)):
            qLog.log('info', main_id, 'srt   = ' + srt_file)
        if (res == True):
            ext = inp_file[-4:].lower()
            if (ext == '.mp4') or (ext == '.m4v'):
                qLog.log('info', main_id, '字幕合成')
                res = qWhisper.jimaku_proc(inp_file, srt_file, out_file, )
                #print(out_file, res)
                qLog.log('info', main_id, 'jimaku=' + str(res))
                if (os.path.exists(out_file)):
                    qLog.log('info', main_id, 'output= ' + out_file)



    # 処理終了
    if (True):
        end_now  = datetime.datetime.now()
        end_time = end_now.strftime('%Y/%m/%d %H:%M:%S')

        qLog.log('info', main_id, 'proctime ' + str(end_now-start_now))
        qLog.log('info', main_id, 'complete!')

    # exit
    if (runMode == 'debug'):
        x = input('Press enter to exit...')

    # 終了処理
    if (True):
        qLog.log('info', main_id, 'terminate')
        qLog.log('info', main_id, 'bye!')

        sys.exit(0)


