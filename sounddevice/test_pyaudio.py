#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://qiita.com/1219mai0410/items/69d89c1a25846af4992d

import pyaudio
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024 * 4
SAMPLE_RATE = 16000

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

while True:
    data = stream.read(CHUNK)   #CHUNKだけデータを読み込む
    line.set_ydata(np.frombuffer(data ,dtype=np.int16) / 2**15)
    fig.canvas.restore_region(bg)   #保存した描画情報を読み込む
    ax.draw_artist(line)   #データを指定
    fig.canvas.blit(ax.bbox)   #保存した描画情報にデータを加える
    fig.canvas.flush_events()   #描画情報をクリア

stream.stop_stream()   #streamを止める
stream.close()   #streamを閉じる
p.terminate()   #pyaudioを終了

