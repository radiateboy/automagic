# -*-coding:utf-8-*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2016-09-03
"""
import requests
import json


def call_post(url_post, para_dict):
    data = json.dumps(para_dict)
    req = requests.post(url_post, data=data)
    if req.status_code != 200:
        print("Failed: HTTP error code: %s" % req.status_code)
        return None
    else:
        return req.text


def call_get(url_get):
    response = requests.get(url_get)
    if response.status_code != 200:
        print("Failed: HTTP error code: %s" % response.status_code)
        return None
    else:
        return response.text


if "__main__" == __name__:
    pass
