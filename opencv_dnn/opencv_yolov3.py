#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://ymgsapo.com/2019/04/05/raspi-opencv-dnn-obj-detection/

import cv2
import numpy as np
import codecs

file_config  = 'yolov3-coco/yolov3-tiny.cfg'
file_weights = 'yolov3-coco/yolov3-tiny.weights'
file_labels  = 'yolov3-coco/coco-labels.txt'

#file_config  = u'C:/Users/kondou/Documents/GitHub/pycv5/yolo3_weights/yolov3.cfg'
#file_weights = u'C:/Users/kondou/Documents/GitHub/pycv5/yolo3_weights/yolov3.weights'

# モデルの読み込み
model = cv2.dnn.readNetFromDarknet(file_config, file_weights)
layer_names = model.getLayerNames()
layer_names = [layer_names[i[0] - 1] for i in model.getUnconnectedOutLayers()]

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
#blob = cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True)
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
model.setInput(blob)

# 画像から物体検出を行う
#output = model.forward()
output = model.forward(layer_names)

# ループ
for detections in output:

    # detectionには[Xの中心点、Yの中心点、Xの幅、Yの幅、クラス別予測確率…]が入っている。
    for detection in detections:

        # クラス別予測確率の最大を取り出す
        scores = detection[5:]
        classid = np.argmax(scores)

        # 予測確率を取り出し0.7以上か判定する。
        confidence = scores[classid]
        if confidence > .7:

            # クラス名を取り出す。
            class_name  = classNames[classid] + ' {0:.2f}'.format(confidence)
            class_color = [ int(c) for c in classColors[classid] ]

            # 検出された物体の名前を表示
            print(class_name)

            # 予測値に元の画像サイズを掛けて、四角で囲むための4点の座標情報を得る
            axis = detection[0:4] * (image_width, image_height, image_width, image_height)

            # floatからintに変換して、変数に取り出す。画像に四角や文字列を書き込むには、座標情報はintで渡す必要がある。
            center_x, center_y, b_width, b_height = axis.astype(np.int)[:4]
            start_x = int(center_x - b_width/2)
            end_x   = int(center_x + b_width/2)
            start_y = int(center_y - b_height/2)
            end_y   = int(center_y + b_height/2)

            # (画像、開始座標、終了座標、色、線の太さ)を指定
            cv2.rectangle(image, (start_x, start_y), (end_x, end_y), class_color, thickness=2)

            # (画像、文字列、開始座標、フォント、文字サイズ、色)を指定
            cv2.putText(image, class_name, (start_x, start_y), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255))

#cv2.imwrite("img/laptop_box_text.jpg", image)
cv2.imshow('image', image)

cv2.waitKey(0)
cv2.destroyAllWindows()


