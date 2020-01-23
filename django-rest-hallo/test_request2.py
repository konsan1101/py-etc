#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import base64



if __name__ == '__main__':

    url = 'http://127.0.0.1:8000/users/'
    id  = 'kondou'
    pw  = 'kondou'

    headers = {
        'Content-Type': 'application/json',
        }
    params = {
        }
    res = requests.get( url=url, 
                        auth=(id, pw), 
                        headers=headers, 
                        params=params, 
                        timeout=15, )

    print(res.status_code)
    print(res.elapsed)

    if (res.status_code == 200):

        res_json  = res.json()
        print( json.dumps(res_json, indent=4, ) )


