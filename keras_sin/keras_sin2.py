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



def _load_data(data, n_prev=30):  
    docX, docY = [], []

    for i in range(len(data) - n_prev):
        docX.append(data.iloc[i:i + n_prev].values)
        docY.append(data.iloc[i + n_prev].values)
    alsX = np.array(docX)
    alsY = np.array(docY)

    return alsX, alsY

def train_test_split(df, test_size=0.1, n_prev=30):  
    ntrn = round(len(df) * (1 - test_size))
    ntrn = int(ntrn)
    X_train, y_train = _load_data(df.iloc[0:ntrn], n_prev)
    X_test, y_test = _load_data(df.iloc[ntrn:], n_prev)

    return (X_train, y_train), (X_test, y_test)



(X_train, y_train), (X_test, y_test) = train_test_split(df[["sin_t"]])



from keras.models import Sequential  
from keras.layers.core import Dense, Activation  
from keras.layers.recurrent import LSTM

# パラメータ
in_out_neurons = 1
hidden_neurons = 300
length_of_sequences = 30

model = Sequential()  
model.add(LSTM(hidden_neurons, batch_input_shape=(None, length_of_sequences, in_out_neurons), return_sequences=False))  
model.add(Dense(in_out_neurons))  
model.add(Activation("linear"))  
model.compile(loss="mean_squared_error", optimizer="rmsprop")
model.fit(X_train, y_train, batch_size=600, nb_epoch=15, validation_split=0.05)



# 予測
predicted = model.predict(X_test)

# 描写
dataf =  pd.DataFrame(predicted[:200])
dataf.columns = ["predict"]
dataf["input"] = y_test[:200]
dataf.plot()


# 画像を保存
plt.savefig('temp_output2.png')


