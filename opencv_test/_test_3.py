#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://note.nkmk.me/python-opencv-image-warping/

import cv2
import numpy as np

def warp(src, dst, src_pts, dst_pts, transform_func, warp_func, **kwargs):
    src_pts_arr = np.array(src_pts, dtype=np.float32)
    dst_pts_arr = np.array(dst_pts, dtype=np.float32)
    src_rect = cv2.boundingRect(src_pts_arr)
    dst_rect = cv2.boundingRect(dst_pts_arr)
    src_crop = src[src_rect[1]:src_rect[1] + src_rect[3], src_rect[0]:src_rect[0] + src_rect[2]]
    dst_crop = dst[dst_rect[1]:dst_rect[1] + dst_rect[3], dst_rect[0]:dst_rect[0] + dst_rect[2]]
    src_pts_crop = src_pts_arr - src_rect[:2]
    dst_pts_crop = dst_pts_arr - dst_rect[:2]

    mat = transform_func(src_pts_crop.astype(np.float32), dst_pts_crop.astype(np.float32))
    warp_img = warp_func(src_crop, mat, tuple(dst_rect[2:]), **kwargs)

    mask = np.zeros_like(dst_crop, dtype=np.float32)
    cv2.fillConvexPoly(mask, dst_pts_crop.astype(np.int), (1.0, 1.0, 1.0), cv2.LINE_AA)

    dst_crop_merge = warp_img * mask + dst_crop * (1 - mask)
    dst[dst_rect[1]:dst_rect[1] + dst_rect[3], dst_rect[0]:dst_rect[0] + dst_rect[2]] = dst_crop_merge

def warp_triangle(src, dst, src_pts, dst_pts, **kwargs):
    warp(src, dst, src_pts, dst_pts,
         cv2.getAffineTransform, cv2.warpAffine, **kwargs)

def warp_rectangle(src, dst, src_pts, dst_pts, **kwargs):
    warp(src, dst, src_pts, dst_pts,
         cv2.getPerspectiveTransform, cv2.warpPerspective, **kwargs)



# 3角形
src = cv2.imread('0.black.jpg')
dst = cv2.imread('0.dog.jpg')

src_pts = [[220, 220], [320, 220], [320, 550]]
dst_pts = [[220, 220], [320, 220], [320, 550]]

warp_triangle(src, dst, src_pts, dst_pts)

cv2.imwrite('9.triangle.jpg', dst)



# 4角形
src = cv2.imread('0.black.jpg')
dst = cv2.imread('0.dog.jpg')

#src_pts = [[220, 220], [320, 220], [320, 550], [120, 550], [120, 360]]
#dst_pts = [[220, 220], [320, 220], [320, 550], [120, 550], [120, 360]]
src_pts = [[220, 220], [320, 220], [320, 550], [120, 550], ]
dst_pts = [[220, 220], [320, 220], [320, 550], [120, 550], ]

warp_rectangle(src, dst, src_pts, dst_pts )

cv2.imwrite('9.rectangle.jpg', dst)


