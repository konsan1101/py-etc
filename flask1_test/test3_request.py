#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://qiita.com/mSpring/items/257adb27d9170da3b372

# localostは遅い！ 127.0.0.1にすること！

import requests

ses = requests.Session()
st = ses.post("http://127.0.0.1:5000/", 
              params={'id':'idididid',
                      'pw':'pwpwpwpw',
                      'mode':'test'})
print('login_status:'+str(st.status_code))

for i in range(0,10000):
    st = ses.get("http://127.0.0.1:5000/count")
    print(st.text)

