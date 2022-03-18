#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://qapicks.com/question/69249813-6065dce8b853

# import Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt

#load image
input_img=cv2.imread("sample2.jpg")

#another function to create blobs
params=cv2.SimpleBlobDetector_Params()
#AREA
params.filterByArea=True
params.minArea=150
#CIRCULARITY
params.filterByCircularity=True
params.minCircularity=0.4
#CONVEXITY
params.filterByConvexity=True
params.minConvexity=0.3
#INERTIA
params.filterByInertia=True
params.minInertiaRatio=0.01

detector=cv2.SimpleBlobDetector_create(params)
keypoints=detector.detect(input_img)
blank=np.zeros((1,1))
number_of_keypoints = len(keypoints)

#for i in range(number_of_blobs):
print("Number of Circular keypoints: " + str(number_of_keypoints))

#drawKeypoints
#output_img=cv2.drawKeypoints(input_img,keypoints,blank,(255,0,255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

#circle
output_img=input_img.copy()
for kp in keypoints:
    #print(kp.pt, kp.size)
    x = int(kp.pt[0])
    y = int(kp.pt[1])
    l = int(kp.size*0.5)
    cv2.circle(output_img, (x,y), l, (255, 0, 255), thickness=-1)

cv2.imshow("matchs",output_img)
cv2.waitKey(0)

cv2.destroyAllWindows()


