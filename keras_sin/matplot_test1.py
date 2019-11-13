#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://qiita.com/trami/items/b501abe7667e55ab2c9f

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()

t  = np.linspace(0, 10, 1000)
t2 = np.linspace(10, 20, 1000)
y1 = np.sin(t)
y2 = np.cos(t2) 

c1,c2, = "blue","green" # 各プロットの色
l1,l2, = "sin","cos"    # 各ラベル

ax.set_xlabel('t')  # x軸ラベル
ax.set_ylabel('y')  # y軸ラベル
ax.set_title('test graph') # グラフタイトル
# ax.set_aspect('equal') # スケールを揃える
ax.grid()            # 罫線
#ax.set_xlim([-10, 10]) # x方向の描画範囲を指定
#ax.set_ylim([0, 1])    # y方向の描画範囲を指定
ax.plot(t, y1, color=c1, label=l1)
ax.plot(t2, y2, color=c2, label=l2)
ax.legend(loc=0)    # 凡例
fig.tight_layout()  # レイアウトの設定
# plt.savefig('hoge.png') # 画像の保存
plt.show()
