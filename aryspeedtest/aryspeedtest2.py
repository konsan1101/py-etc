#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

if __name__ == '__main__':

    lp = 10000

    print("init")

    arydiv = []
    for x in range(1,lp):
        aryyyy = []
        for y in range(1,lp):
            n = int( x / y )
            aryyyy.append(n)
            #print(x,y)
        arydiv.append(aryyyy)

    print("div")

    st = time.time()
    for x in range(1,lp):
        for y in range(1,lp):
            n = int( x / y )
    en = time.time()

    print("…", en-st)

    print("ary")

    st = time.time()
    for x in range(1,lp):
        for y in range(1,lp):
            n = arydiv[x-1][y-1]
    en = time.time()

    print("…", en-st)
