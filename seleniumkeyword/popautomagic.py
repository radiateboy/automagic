# -*- coding: utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2017-03-01
"""

import requests, json


def sendAutoMagic(url, data):

    headers = {"Content-Type": "application/json"}
    requests.post(url, data=data, headers=headers)


# call_post(url_post, data_text)


if '__main__' == __name__:
    #MWQA
    url_post = "https://oapi.dingtalk.com/robot/send?access_token=8d36288c964c024ca2e5e53a45faddde0adcb2c6c638e9a59a16096f5d866715"
    #Test
    #url_post = "https://oapi.dingtalk.com/robot/send?access_token=e0c23e2f9242783f0ad34ccf21197a41f663c9b63ddc87fc386722654914c7ee"

    data_text = json.dumps({
        "msgtype": "text",
        "text": {
            "content": "圈人"
        },
        "at": {
            "atMobiles": [
                "18217516787",#wenjuang.wang
                "15891390680" #yongbo.he
            ],
            "isAtAll": False
        }
    })

    data_link = json.dumps({"msgtype": "link",
                            "link": {
                                "text": "这个即将发布的新版本，创始人陈航（花名“无招”）称它为“红树林”。而在此之前，每当面临重大升级，产品经理们都会取一个应景的代号，这一次，为什么是“红树林”？",
                                "title": "时代的火车向前开", "picUrl": "",
                                "messageUrl": "https://mp.weixin.qq.com/s?__biz=MzA4NjMwMTA2Ng==&mid=2650316842&idx=1&sn=60da3ea2b29f1dcc43a7c8e4a7c97a16&scene=2&srcid=09189AnRJEdIiWVaKltFzNTw&from=timeline&isappinstalled=0&key=&ascene=2&uin=&devicetype=android-23&version=26031933&nettype=WIFI"}
                            })

    count_num, pass_num, fail_num, error_num = 631, 328, 101, 202
    data_markdown = json.dumps({
        "msgtype": "markdown",
        "markdown": {
            "title": "AutoMagic TestReprot",
            "text": "![screenshot](http://192.168.110.65/static/images/automagic.png) \n" +
                    ">[AutoMagic TestReprot](http://jenkinsm.acorn-net.com/TestResults/CornerStone/2017-02-19/2017-02-19-00_55_46_result.html) \n\n " +
                    ">执行CASE" + str(count_num) + "个，Pass" + str(pass_num) + "个，Fail" + str(fail_num) + "个，Error" + str(
                error_num) + "个\n"
            }
    })
    data_md = json.dumps({
        "msgtype": "markdown",
        "markdown": {
            "title": "Script Update",
            "text": "![screenshot](http://192.168.110.65/static/images/automagic.png) \n" +
                    ">[192.168.115.1](\\192.168.115.1) \n\n " +
                    ">sendingdata.py 脚本更新\n" +
                    ">1.添加 -t 参数调整线程数量，默认为1\n"
                    ">2.添加 -s 参数调整发包速度（单位是秒）可以是小数\n"
        }
    })
    data_test = '''{"msgtype": "text", "text": {"content": "我就是我,颜色不一样的烟火!!!"}}'''
    sendAutoMagic(url_post, data_md)
