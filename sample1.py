#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

# ----------------
# 古典的コーディング（ループ）
# ----------------
suu = [ 1, 2, 3, ]
tan = [ 100, 200, 300, ]
kin = [ 0, 0, 3, ]
for i in range(3):
    kin[i] = suu[i] * tan[i]
print(kin)

# ----------------
# 現代的コーディング（行列一括計算）
# ----------------
suu = np.array([ 1, 2, 3, ])
tan = np.array([ 100, 200, 300, ])
kin = suu * tan
print(kin)


