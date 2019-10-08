#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://qiita.com/ReoNagai/items/4c5c2c2b1175f898c0d6

import numpy as np
import gym
import random

from collections import deque
from keras.layers import Input, Activation, Dense, Flatten, RepeatVector, Reshape
from keras.layers.convolutional import Conv2D
from keras.models import Model
from keras import backend as K

import cv2
from skimage.color import rgb2gray
from skimage.transform import resize
# rmsprop
import keras

np.set_printoptions(suppress=True)

resize_x = 84
resize_y = 84

file_history = open("test3_history.txt", "w")
file_history.close()


class Agent:
    def __init__(self, env):
        self.env = env
        self.input_dim = env.observation_space.shape
        self.output_dim = env.action_space.n

        self.q_network = self.ModelCreate()
        self.t_network = self.ModelCreate()

        self.t_network.load_weights("test3_weight.h5") # 初期の重みを考慮する場合
        self.q_network.summary()
        self.max_q = 0

    def ModelCreate(self):
        ip = Input(shape=(resize_y, resize_x, 1))
        h = Conv2D(32, (4,4),strides=(2,2),padding="same",activation='relu')(ip)
        h = Conv2D(64,(4,4),strides=(4,4),padding="same",activation='relu')(h)
        h = Conv2D(64,(3,3),strides=(3,3),padding="same",activation='relu')(h)
        h = Flatten()(h)
        h = Dense(512, activation='relu')(h)
        h = Dense(self.output_dim)(h)
        model = Model(ip, output=h)

        rmsprop = keras.optimizers.RMSprop(lr=0.00025, rho=0.95, epsilon=0.01, decay=0.0)
        model.compile(rmsprop, 'mse')
        return model

    def getAction(self, state, epsilon):
        # epsilon-greedy
        if np.random.rand() < epsilon:
            return self.env.action_space.sample()

        state = state[np.newaxis,:,:,:]
        # -20191008
        #q_value = self.q_network.predict_on_batch(state)
        # 20191008-
        q_value = self.Predict(state)
        return np.argmax(q_value)

    def Train(self, x_batch, y_batch):
        return self.q_network.train_on_batch(x_batch, y_batch)

    def Predict(self, x_batch):
        return self.t_network.predict_on_batch(x_batch)

    def WeightCopy(self):
        for i in range(7):
            self.t_network.layers[i].set_weights(self.q_network.layers[i].get_weights())
        #self.t_network.set_weights(self.q_network.get_weights())

    # 学習の結果を保存しておく
    def SaveHistory(self, episode, reward, epsilon, next_state):
        next_state = next_state[np.newaxis,:,:,:]
        predict = self.Predict(next_state)

        msg = "[episode:" + str(episode) + " } {reward:" + str(reward) + "} {epsilon:" + str(epsilon) + "}]"
        msg_all = str(predict.max()) + " action[" + str(predict.argmax()) + "] max_q(" + str(self.max_q) + ")\t" + str(predict) + " \t" + msg + "\n"

        print(msg_all)
        # 保存
        file_history = open("test3_history.txt", "a")
        file_history.write(msg_all)
        file_history.close()


def CreateBatch(agent, replay_memory, batch_size, discount_rate):
    minibatch = random.sample(replay_memory, batch_size)
    state, action, reward, state2, end_flag =  map(np.array, zip(*minibatch))

    x_batch = state
    # この状態の時に各行動をした場合のQ値(y_batch変数はactionそれぞれに対するQ値)を，現在のネットワークで推定
    y_batch = agent.Predict(state)
    # 今のQ値よりももっと高かったら更新
    agent.max_q = max(agent.max_q, y_batch.max()) # 保存用
    # 1つ未来における各行動に対するそれぞれのQ値
    next_q_values = agent.Predict(state2)

    for i in range(batch_size):
        # ベルマン方程式 Q(s,a) = r + gamma * max_a Q(s', a') 
        y_batch[i, action[i]] = reward[i] + discount_rate * np.max(next_q_values[i]) * (1 - end_flag[i])

    return x_batch, y_batch


def PrintInfo(episode, reward, epsilon):
    msg = "[episode:" + str(episode) + " } {reward:" + str(reward) + "} {epsilon:" + str(epsilon) + "}]"
    print(msg)


def RewardClipping(reward):
    return np.sign(reward)

def Preprocess(image, _resize_x=resize_x, _resize_y=resize_y):
    gray_image = rgb2gray(image)
    gray_image = resize(gray_image, (_resize_x, _resize_y))
    return gray_image[:,:,np.newaxis]

def main():
    n_episode = 1000
    discount_rate = 0.99
    max_memory = 20000
    batch_size = 32
    epsilon = 1.0
    min_epsilon = 0.1
    reduction_epsilon = (1. - min_epsilon) / n_episode

    #env_name = 'CartPole-v0'
    env_name = 'Breakout-v0'
    env = gym.make(env_name)
    agent = Agent(env)
    replay_memory = deque()

    # ゲーム再スタート
    for episode in range(n_episode):
        episode_reward = 0
        end_flag = False
        epsilon -= reduction_epsilon

        state = env.reset()
        state = Preprocess(state, resize_x, resize_y)

        epsilon = min_epsilon + (1. - min_epsilon) * (n_episode - episode) / n_episode
        # ボールが落ちるまで
        while not end_flag:
            action = agent.getAction(state, epsilon)
            state2, reward, end_flag, info = env.step(action)
            # 前処理
            state2 = Preprocess(state2, resize_x, resize_y)
            episode_reward += reward
            # 報酬のクリッピング
            reward = RewardClipping(reward)

            # リプレイメモリに保存
            replay_memory.append([state, action, reward, state2, end_flag])
            # リプレイメモリが溢れたら前から削除
            if len(replay_memory) > max_memory:
                replay_memory.popleft()
            # リプレイメモリが溜まったら学習
            #if len(replay_memory) > batch_size*2:
            if len(replay_memory) > max_memory/2 :
                x_batch, y_batch = CreateBatch(agent, replay_memory, batch_size, discount_rate)
                #print(y_batch)
                agent.Train(x_batch, y_batch)

            state = state2
            # 可視化
            #env.render()
        # Q-networkの重みをTarget-networkにコピー
        agent.WeightCopy()
        if episode != 0 and episode % 1 == 0:
            agent.t_network.save_weights("test3_weight.h5")

        #PrintInfo(episode, episode_reward, epsilon)

        agent.SaveHistory(episode, episode_reward, epsilon, state2)

    env.close()


if __name__ == '__main__':
    main()


