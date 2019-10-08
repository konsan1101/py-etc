#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://ymgsapo.com/2019/04/05/raspi-opencv-dnn-obj-detection/

import cv2
import numpy as np
import codecs

file_config  = 'ssd/frozen_inference_graph.pb'
file_weights = 'ssd/ssd_mobilenet_v2_coco_2018_03_29.pbtxt'
file_labels  = 'ssd/labels.txt'
threshold_score = 0.5
threshold_nms   = 0.4

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
image_height, image_width = image.shape[:2]

# 入力画像成形
if (image_width > image_height):
    image_size = image_width
    inp_image = np.zeros((image_width,image_width,3), np.uint8)
    offset = int((image_width-image_height)/2)
    inp_image[offset:offset+image_height, 0:image_width] = image.copy()
    out_image = inp_image.copy()
elif (image_height > image_width):
    image_size = image_height
    inp_image = np.zeros((image_height,image_height,3), np.uint8)
    offset = int((image_height-image_width)/2)
    inp_image[0:image_height, offset:offset+image_width] = image.copy()
    out_image = inp_image.copy()
else:
    image_size = image_width
    inp_image = image.copy()
    out_image = inp_image.copy()

# Imageをセットする
blob = cv2.dnn.blobFromImage(inp_image, size=(300, 300), swapRB=True)
model.setInput(blob)

# 画像から物体検出を行う
output = model.forward()

pass_classids = []
pass_scores   = []
pass_boxes    = []

# outputは[1:1:100:7]のリストになっているため、後半の2つを取り出す
detections = output[0, 0, :, :]

# detectionには[?,id番号、予測確率、Xの開始点、Yの開始点、Xの終了点、Yの終了点]が入っている。
for detection in detections:

    # 予測確率がthreshold_score以上を取り出す。
    score = detection[2]
    if (score >= threshold_score):

        # 元の画像サイズを掛けて、四角で囲むための4点の座標情報を得る
        axis = detection[3:7] * (image_size, image_size, image_size, image_size)

        # floatからintに変換して、変数に取り出す。
        (start_x, start_y, end_x, end_y) = axis.astype(np.int)[:4]
        left   = int(start_x)
        top    = int(start_y)
        width  = int(end_x - start_x)
        height = int(end_y - start_y)

        # 変数に取り出す。
        if (width>=10) and ((height)>=10):
            classid = detection[1]
            pass_classids.append(classid)
            pass_scores.append(float(score))
            pass_boxes.append([left, top, width, height])

# 重複した領域を排除した内容を利用する。
indices = cv2.dnn.NMSBoxes(pass_boxes, pass_scores, float(threshold_score), float(threshold_nms))
for i in indices:
    i = i[0]
    classid = pass_classids[i]
    score   = pass_scores[i]
    box     = pass_boxes[i]
    left    = box[0]
    top     = box[1]
    width   = box[2]
    height  = box[3]

    # クラス名を取り出す。
    class_name  = classNames[classid]
    class_color = [ int(c) for c in classColors[classid] ]
    label       = class_name + ' {0:.2f}'.format(score)

    # 検出された物体の名前を表示
    print(label)

    # (画像、開始座標、終了座標、色、線の太さ)を指定
    cv2.rectangle(out_image, (left, top), (left+width, top+height), class_color, thickness=2)

    # (画像、文字列、開始座標、フォント、文字サイズ、色)を指定
    t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX_SMALL, 1 , 1)[0]
    x = left + t_size[0] + 3
    y = top + t_size[1] + 4
    cv2.rectangle(out_image, (left, top), (x, y), class_color, -1)
    cv2.putText(out_image, label, (left, top + t_size[1] + 1), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,255,255), 1)

# 出力画像復元
if (image_width > image_height):
    offset = int((image_width-image_height)/2)
    out_image = out_image[offset:offset+image_height, 0:image_width].copy()
elif (image_height > image_width):
    image_size = image_height
    offset = int((image_height-image_width)/2)
    out_image = out_image[0:image_height, offset:offset+image_width].copy()

cv2.imshow('image', out_image)

cv2.waitKey(0)
cv2.destroyAllWindows()


