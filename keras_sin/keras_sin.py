#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://qiita.com/kazukiii/items/df809d6cd5d7d1f57be3


import pandas as pd
import numpy as np
import math
import random
import matplotlib.pyplot as plt
import seaborn as sns

# サイクルあたりのステップ数
steps_per_cycle = 80

# 生成するサイクル数
number_of_cycles = 50

df = pd.DataFrame(np.arange(steps_per_cycle * number_of_cycles + 1), columns=["t"])
# 一様乱数でノイズを発生させたsin波を生成
df["sin_t"] = df.t.apply(lambda x: math.sin(x * (2 * math.pi / steps_per_cycle)+ random.uniform(-0.05, +0.05) ))
# 2サイクルだけ抽出してプロット
df[["sin_t"]].head(steps_per_cycle * 2).plot()
# 画像を保存
plt.savefig('temp_output1.png')





