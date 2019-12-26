#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://note.nkmk.me/python-opencv-image-warping/

import cv2
import numpy as np

src = cv2.imread('0.black.jpg')
dst = cv2.imread('0.dog.jpg')

#src_pts = [[220, 220], [320, 220], [320, 550], [120, 550], [120, 360]]
#dst_pts = [[220, 220], [320, 220], [320, 550], [120, 550], [120, 360]]
src_pts = [[220, 220], [320, 220], [320, 550]]
dst_pts = [[220, 220], [320, 220], [320, 550]]



# srcマーク
src_mark = src.copy()

for pt in src_pts:
    cv2.drawMarker(src_mark, tuple(pt), (0, 255, 0), thickness=4)

cv2.imwrite('1.src_mark.jpg', src_mark)

# dstマーク
dst_mark = dst.copy()

for pt in dst_pts:
    cv2.drawMarker(dst_mark, tuple(pt), (0, 255, 0), thickness=4)

cv2.imwrite('1.dst_mark.jpg', dst_mark)

# バウンディングボックスで切り出し
src_pts_arr = np.array(src_pts, dtype=np.float32)
dst_pts_arr = np.array(dst_pts, dtype=np.float32)

src_rect = cv2.boundingRect(src_pts_arr)
dst_rect = cv2.boundingRect(dst_pts_arr)

print(src_rect)
print(dst_rect)

src_crop = src[src_rect[1]:src_rect[1] + src_rect[3], src_rect[0]:src_rect[0] + src_rect[2]]
dst_crop = dst[dst_rect[1]:dst_rect[1] + dst_rect[3], dst_rect[0]:dst_rect[0] + dst_rect[2]]

src_pts_crop = src_pts_arr - src_rect[:2]
dst_pts_crop = dst_pts_arr - dst_rect[:2]

print(src_pts_crop)
print(dst_pts_crop)

# 切り出し画像に座標にマークを描画
src_crop_mark = src_crop.copy()
for pt in src_pts_crop.astype(np.int):
    cv2.drawMarker(src_crop_mark, tuple(pt), (0, 255, 0), thickness=4)
cv2.imwrite('2.src_crop_mark.jpg', src_crop_mark)

dst_crop_mark = dst_crop.copy()
for pt in dst_pts_crop.astype(np.int):
    cv2.drawMarker(dst_crop_mark, tuple(pt), (0, 255, 0), thickness=4)
cv2.imwrite('2.dst_crop_mark.jpg', dst_crop_mark)

# 切り出し画像に対してアフィン変換
mat = cv2.getAffineTransform(src_pts_crop.astype(np.float32), dst_pts_crop.astype(np.float32))
affine_img = cv2.warpAffine(src_crop, mat, tuple(dst_rect[2:]))
cv2.imwrite('3.affine_crop.jpg', affine_img)

# 切り出し画像をマスク処理して合成
mask = np.zeros_like(dst_crop, dtype=np.float32)
cv2.fillConvexPoly(mask, dst_pts_crop.astype(np.int), (1.0, 1.0, 1.0), cv2.LINE_AA)
dst_crop_merge = affine_img * mask + dst_crop * (1 - mask)
cv2.imwrite('4.affine_crop_merge.jpg', dst_crop_merge)

# 結果出力
dst[dst_rect[1]:dst_rect[1] + dst_rect[3], dst_rect[0]:dst_rect[0] + dst_rect[2]] = dst_crop_merge
cv2.imwrite('9.dst_result.jpg', dst)


