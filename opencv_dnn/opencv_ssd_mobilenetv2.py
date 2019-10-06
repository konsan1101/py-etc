#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://ymgsapo.com/2019/04/05/raspi-opencv-dnn-obj-detection/

import cv2
import numpy as np
import codecs

file_config  = 'ssd_mobilenetv2/frozen_inference_graph.pb'
file_weights = 'ssd_mobilenetv2/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
file_labels  = 'ssd_mobilenetv2/labels.txt'

# モデルの読み込み
model = cv2.dnn.readNetFromTensorflow(file_config, file_weights)

# モデルの中の訓練されたクラス名
classNames  = {}
classColors = {}
r = codecs.open(file_labels, 'r', 'utf-8')
i = 0
for t in r:
    t = t.replace('\n', '')
    t = t.replace('\r', '')
    classNames[i]  = str(t).strip()
    classColors[i] = np.random.randint(low=0, high=255, size=3, dtype='uint8')
    i += 1

# テスト画像の読み込み
image = cv2.imread("dog.jpg")

# 画像の縦と横サイズを取得
image_height, image_width = image.shape[:2]

# Imageをセットする
blob = cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True)
model.setInput(blob)

# 画像から物体検出を行う
output = model.forward()

# outputは[1:1:100:7]のリストになっているため、後半の2つを取り出す
detections = output[0, 0, :, :]

# detectionには[?,id番号、予測確率、Xの開始点、Yの開始点、Xの終了点、Yの終了点]が入っている。
for detection in detections:

    # 予測確率を取り出し0.7以上か判定する。
    confidence = detection[2]
    if confidence > .7:

        # id番号を取り出し、辞書からクラス名を取り出す。
        classid = detection[1]
        class_name  = classNames[classid] + ' {0:.2f}'.format(confidence)
        class_color = [ int(c) for c in classColors[classid] ]

        # 検出された物体の名前を表示
        print(class_name)

        # 予測値に元の画像サイズを掛けて、四角で囲むための4点の座標情報を得る
        axis = detection[3:7] * (image_width, image_height, image_width, image_height)

        # floatからintに変換して、変数に取り出す。画像に四角や文字列を書き込むには、座標情報はintで渡す必要がある。
        (start_x, start_y, end_x, end_y) = axis.astype(np.int)[:4]

        # (画像、開始座標、終了座標、色、線の太さ)を指定
        cv2.rectangle(image, (start_x, start_y), (end_x, end_y), class_color, thickness=2)

        # (画像、文字列、開始座標、フォント、文字サイズ、色)を指定
        cv2.putText(image, class_name, (start_x, start_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))

#cv2.imwrite("img/laptop_box_text.jpg", image)
cv2.imshow('image', image)

cv2.waitKey(0)
cv2.destroyAllWindows()


