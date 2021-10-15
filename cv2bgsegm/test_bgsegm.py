#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://pystyle.info/opencv-background-substraction/

import cv2

cap = cv2.VideoCapture("vtest.avi")
wait_secs = int(1000 / cap.get(cv2.CAP_PROP_FPS))

model = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    mask = model.apply(frame)

    cv2.imshow("Mask", mask)
    cv2.waitKey(wait_secs)

cap.release()
cv2.destroyAllWindows()


