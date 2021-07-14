#!/usr/bin/env python
# -*- coding: utf-8 -*-

import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Images
imgs = ['dog.jpg']  # batch of images

# Inference
results = model(imgs)

# Results
results.print()
#results.show()
results.save()

results.xyxy[0]  # img1 predictions (tensor)
results.pandas().xyxy[0]  # img1 predictions (pandas)



