# -*-coding:utf-8-*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2016-09-03
"""
import urllib
import urllib2
import json


def call_post(url_post, para_dict):
    data = json.dumps(para_dict)
    req = urllib2.Request(url_post, data)
    response = urllib2.urlopen(req)

    if response.getcode() != 200:
        print "Failed: HTTP error code: %s" % response.getcode()
        return None
    else:
        return response.read()


def call_get(url_get):
    response = urllib.urlopen(url_get)
    if response.getcode() != 200:
        print "Failed: HTTP error code: %s" % response.getcode()
        return None
    else:
        return response.read()


if "__main__" == __name__:
    pass
