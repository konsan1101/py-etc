#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time, random
from xgoogle.search import GoogleSearch, SearchError

for i in range(0,2):
    wt = random.uniform(2, 5)
    gs = GoogleSearch("about")
    gs.results_per_page = 10
    gs.page = i
    results = gs.get_results()
    #Try not to annnoy Google, with a random short wait
    time.sleep(wt)
    #print 'This is the %dth iteration and waited %f seconds' % (i, wt)
    for res in results:
        print(res.url.encode("utf8"))


