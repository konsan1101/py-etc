#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://qiita.com/Umaremin/items/4317fb88299995e54e5f

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn import preprocessing
from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM

from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split

# データ読み込み
df = pd.read_csv("nikkei_stock_average_daily_jp.csv")
df['date'] = pd.to_datetime(df['date'], format = '%Y-%m-%d')

#データの標準化
df2 = df.loc[:, ['date', 'close']]
df2['close'] = preprocessing.scale(df2['close'])
#dfx = []
#for val in df2['close']:
#    dfx.append(val/30000)
#df2['close'] = dfx

#訓練、テストデータの作成
maxlen = 10
X, Y = [], []
for i in range(len(df2) - maxlen):
    X.append(df2[['close']].iloc[i:(i+maxlen)].as_matrix())
    Y.append(df2[['close']].iloc[i+maxlen].as_matrix())
X=np.array(X)
Y=np.array(Y)

# 訓練用のデータと、テスト用のデータに分ける
N_train = int(len(df2) * 0.8)
N_test = len(df2) - N_train
X_train, X_test, y_train, y_test = \
    train_test_split(X, Y, test_size=N_test, shuffle = False) 

# 隠れ層の数などを定義: 隠れ層の数が大きいほど精度が上がる?
n_in = 1 # len(X[0][0])
n_out = 1 # len(Y[0])
n_hidden = 300

#モデル作成 (Kerasのフレームワークで簡易に記載できる)
model = Sequential()
model.add(LSTM(n_hidden,
               batch_input_shape=(None, maxlen, n_in),
               kernel_initializer='random_uniform',
               return_sequences=False))
model.add(Dense(n_in, kernel_initializer='random_uniform'))
model.add(Activation("linear"))

opt = Adam(lr=0.001, beta_1=0.9, beta_2=0.999)
model.compile(loss = "mean_squared_error", optimizer=opt)

early_stopping = EarlyStopping(monitor='loss', patience=10, verbose=1)
hist = model.fit(X_train, y_train, batch_size=maxlen, epochs=500,
                 callbacks=[early_stopping])

# 損失のグラフ化
loss = hist.history['loss']
epochs = len(loss)
plt.rc('font', family='serif')
fig = plt.figure()
fig.patch.set_facecolor('white')
plt.plot(range(epochs), loss, marker='.', label='loss(training data)')
plt.show()

# 予測結果
predicted = model.predict(X_test)
result = pd.DataFrame(predicted)
result.columns = ['predict']
result['actual'] = y_test
result.plot()
plt.show()


