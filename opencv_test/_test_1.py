#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://note.nkmk.me/python-opencv-draw-function/

import cv2
import numpy as np



# 多角形
dst = cv2.imread('0.dog.jpg')
pts = np.array(((220, 220), (320, 220), (320, 550), (120, 550), (120, 360)))

#cv2.polylines(dst, [pts], isClosed=True, color=(0,0,0), thickness=2, )
cv2.fillPoly(dst, [pts], color=(0,0,0), )

cv2.imwrite('9.fillPoly.jpg', dst)


