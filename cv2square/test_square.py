#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://pynote.hatenablog.com/entry/opencv-contour-manipulation

import cv2
import numpy as np

# 読込
#img = cv2.imread("sample0.jpg")
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = cv2.imread("sample1.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#img = cv2.imread("sample2.jpg")
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray = cv2.bitwise_not(gray)

# 変換
cv2.imshow('gray', gray)
_, thresh = cv2.threshold(gray, 192, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('thresh', thresh)
thresh_not = cv2.bitwise_not(thresh)
cv2.imshow('thresh_not', thresh_not)

cv2.waitKey(1)

# 輪郭抽出
contours, hierarchy = cv2.findContours(thresh_not, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 輪郭の周囲の長さを計算する。
#for i, cnt in enumerate(contours):
#    arclen = cv2.arcLength(cnt, True)
#    print('arc length of contour {}: {:.2f}'.format(i, arclen))

# 輪郭の面積を計算する。
#for i, cnt in enumerate(contours):
#    area = cv2.contourArea(cnt)
#    print('contour: {}, area: {}'.format(i, area))

#approx_contours = []
#for i, cnt in enumerate(contours):
#    # 輪郭の周囲の長さを計算する。
#    arclen = cv2.arcLength(cnt, True)
#    # 輪郭を近似する。
#    approx_cnt = cv2.approxPolyDP(cnt, epsilon=0.005 * arclen, closed=True)
#    approx_contours.append(approx_cnt)
#    # 元の輪郭及び近似した輪郭の点の数を表示する。
#    print('contour {}: {} -> {}'.format(i, len(cnt), len(approx_cnt)))

# 幾何図形取得
square_contours = []
for i, cnt in enumerate(contours):

    # 面積で選別
    area = cv2.contourArea(cnt)
    if (area > 5000):

        # 輪郭長さで輪郭を近似化する。
        arclen = cv2.arcLength(cnt, True)
        epsilon_len = arclen * 0.05
        approx_cnt = cv2.approxPolyDP(cnt, epsilon=epsilon_len, closed=True)

        # 画数で選別
        if (len(approx_cnt) == 4):
        #if (True):

            # 輪郭に外接する回転した長方形を取得
            #rect = cv2.minAreaRect(approx_cnt)
            #rect_points = cv2.boxPoints(rect)
            #square_contours.append(rect_points)

            # 座標ずらす
            x = np.array([])
            y = np.array([])
            for i in range(4):
                x = np.append(x, approx_cnt[i][0][0])
                y = np.append(y, approx_cnt[i][0][1])
            ave_x = np.mean(x)
            ave_y = np.mean(y)

            hit1 = False
            hit2 = False
            hit3 = False
            hit4 = False
            for i in range(4):
                if (x[i] <= ave_x) and (y[i] <= ave_y):
                    hit1 = True
                    approx_cnt[0][0][0]=x[i]
                    approx_cnt[0][0][1]=y[i]
                if (x[i] <= ave_x) and (y[i] > ave_y):
                    hit2 = True
                    approx_cnt[1][0][0]=x[i]
                    approx_cnt[1][0][1]=y[i]
                if (x[i] > ave_x) and (y[i] > ave_y):
                    hit3 = True
                    approx_cnt[2][0][0]=x[i]
                    approx_cnt[2][0][1]=y[i]
                if (x[i] > ave_x) and (y[i] <= ave_y):
                    hit4 = True
                    approx_cnt[3][0][0]=x[i]
                    approx_cnt[3][0][1]=y[i]

            if  (hit1 == True) and (hit2 == True) \
            and (hit3 == True) and (hit4 == True):
                square_contours.append(approx_cnt)



# プロット画像表示

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

fig, ax = plt.subplots(figsize=(8, 8))
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
ax.imshow(img_rgb)  # 画像を表示する。
ax.set_axis_off()

for i, cnt in enumerate(square_contours):
    # 形状を変更する。(NumPoints, 1, 2) -> (NumPoints, 2)
    cnt = cnt.squeeze(axis=1)
    # 輪郭の点同士を結ぶ線を描画する。
    ax.add_patch(Polygon(cnt, color='b', fill=None, lw=2))
    # 輪郭の点を描画する。
    ax.plot(cnt[:, 0], cnt[:, 1], 'ro', mew=0, ms=4)
    # 輪郭の番号を描画する。
    ax.text(cnt[0][0], cnt[0][1], i, color="orange", size="20")

#plt.show()



# 投射画像表示

import numpy as np

for i, cnt in enumerate(square_contours):

    dst = []
    pts1 = np.float32(square_contours[i])
    pts2 = np.float32([[0,0],[0,400],[640,400],[640,0]])

    M = cv2.getPerspectiveTransform(pts1,pts2)
    dst = cv2.warpPerspective(img,M,(640,400))
    cv2.imshow('Display'+str(i), dst)
    cv2.waitKey(1)



plt.show()


