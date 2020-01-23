#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import base64



if __name__ == '__main__':

    idpw = 'kondou:kondou'
    #idpw_b64 = base64.b64encode(idpw.encode('utf-8'))
    idpw_b64 = base64.b64encode(idpw.encode('utf-8')).decode('utf-8')
    print(idpw_b64)
    print('')

    url  = 'http://127.0.0.1:8000/users/'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + idpw_b64,
        }
    params = {
        }
    res = requests.get(url, headers=headers, params=params, 
          timeout=15, )
    #res = requests.post(url, headers=headers, params=params, 
    #      data=json.dumps(json_data), timeout=15, )

    print(res.status_code)
    print(res.elapsed)

    if (res.status_code == 200):

        res_json  = res.json()
        print( json.dumps(res_json, indent=4, ) )


