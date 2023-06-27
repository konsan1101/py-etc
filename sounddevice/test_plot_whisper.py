#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://qiita.com/1219mai0410/items/69d89c1a25846af4992d
# https://tadaoyamaoka.hatenablog.com/entry/2022/10/15/175722

import pyaudio
import numpy as np
import matplotlib.pyplot as plt

import whisper
import threading
import queue
import argparse
import time



LANGAGE       = 'ja'
SAMPLE_RATE   = 16000
CHUNK         = 4096
AUDIO_SEC     = 1
AUDIO_BUFFER  = SAMPLE_RATE * AUDIO_SEC
SPEECH_SEC    = 30
SPEECH_BUFFER = SAMPLE_RATE * SPEECH_SEC



pa = pyaudio.PyAudio()

for i in range(pa.get_device_count()):
    print(pa.get_device_info_by_index(i))

stream = pa.open(format=pyaudio.paInt16,   #データの型
                channels=1, #ステレオかモノラルかの選択 1でモノラル 2でステレオ
                rate=SAMPLE_RATE,  #サンプリングレート
                input=True,
                input_device_index = 0,   #マイクの指定
                frames_per_buffer=CHUNK)   #データ数

fig, ax = plt.subplots()   #描画領域の作成
fig.canvas.draw()   #figureの描画
bg = fig.canvas.copy_from_bbox(ax.bbox)   #描画情報を保存
line, = ax.plot([0 for _ in range(CHUNK)])   #データがないためCHANKの数だけ0をplot
ax.set_ylim(-1, 1)   #yのデータ範囲を-1~1に設定
fig.show()   #描画



parser = argparse.ArgumentParser()
#parser.add_argument('--model', default='large-v2')
parser.add_argument('--model', default='small')
args = parser.parse_args()

print('Loading model...')
whisper_model = whisper.load_model(args.model)
options = whisper.DecodingOptions(fp16 = False)
print('Done')

q = queue.Queue()



def recognize():
    while True:
        wave = q.get()
        if (len(wave) > 0):
            audio = whisper.pad_or_trim(wave)

            # make log-Mel spectrogram and move to the same device as the model
            mel_model = whisper.log_mel_spectrogram(audio).to(whisper_model.device)

            # detect the spoken language
            _, probs_model = whisper_model.detect_language(mel_model)
            #print(LANGAGE, probs_model[LANGAGE])

            # decode the audio
            result_model = whisper.decode(whisper_model, mel_model, options, language=LANGAGE, )

            # print the recognized text
            if (result_model.text != '') and (result_model.text[:14] != 'ご視聴ありがとうございました'):
                print(f'{max(probs_model, key=probs_model.get)}: {result_model.text}')

        time.sleep(0.5)

th_recognize = threading.Thread(target=recognize, daemon=True)
th_recognize.start()



a = 0
audio_data  = np.empty(AUDIO_BUFFER * 2, dtype=np.float32)
s = 0
speech_data = np.empty(SPEECH_BUFFER * 2, dtype=np.float32)

onece = True
while True:

    a = 0
    while a < AUDIO_BUFFER:
        wave = stream.read(CHUNK)   #CHUNKだけデータを読み込む
        line.set_ydata(np.frombuffer(wave ,dtype=np.int16) / 2**15)
        fig.canvas.restore_region(bg)   #保存した描画情報を読み込む
        ax.draw_artist(line)   #データを指定
        fig.canvas.blit(ax.bbox)   #保存した描画情報にデータを加える
        fig.canvas.flush_events()   #描画情報をクリア

        audio_data[a:a+CHUNK] = np.frombuffer(wave ,dtype=np.int16) / 2**15
        a += len(wave)

    if ((audio_data[:a] ** 2).max() <= 0.001) or (onece == True):
        onece = False
        print('...')
        a = 0
        if (s != 0):
            print('recognize... '+ str(s))
            q.put(speech_data[:s])
            s = 0

    else:
        print('+++')
        speech_data[s:s+a] = audio_data[:a]
        s += a
        a = 0        
        if (s >= SPEECH_BUFFER):
            print('recognize... '+ str(s))
            q.put(speech_data[:s])
            s = 0

stream.stop_stream()   #streamを止める
stream.close()   #streamを閉じる
p.terminate()   #pyaudioを終了

