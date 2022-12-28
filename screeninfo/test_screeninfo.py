#!/usr/bin/env python
# -*- coding: utf-8 -*-

#https://pypi.org/project/screeninfo/

import screeninfo

for m in screeninfo.get_monitors():
    print(str(m))



