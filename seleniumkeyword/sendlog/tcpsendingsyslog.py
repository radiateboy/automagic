# -*- coding: utf-8 -*-
__author__ = 'Ray'

"""
socket tcp send 发包工具.
mail：tsbc@vip.qq.com
2017-03-03
"""

import sys

import socket
import threading
import argparse

class Controller(object):
    count = 1
    @classmethod
    def init(cls):
        cls.args = get_args()
        cls.thread_stop = False

def get_args():
    '''
    解析命令行参数
    :return: 命令行参数命名空间
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', action='store', dest='host', type=str, help='receive host ip')
    parser.add_argument('-port', action='store', dest='dport', type=str, help='send port')
    parser.add_argument('-c', action='store', dest='count', type=str, help='count number')
    # parser.add_argument('-f', action='store', dest='file', type=str, help='packets file')
    # parser.add_argument('-t', action='store', dest='thread', type=str, help='thread number')
    rst = parser.parse_args()
    return rst

def run(host,port,data,count):
    address = (host, port)
    for i in xrange(count):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(address)
        s.send(data)
        # source = s.recv(1024)
        # print 'the data received is', source
        s.close()


def senddata():
    data = '''<188> 2017-02-27 17:29:30 %SYS-5-CONFIG_I: Configured from console by admin on vty0 (10.0.1.49)'''
    if Controller.args.host is None:
        print "Receiver IP(host) is Null!"
        return False
    else:
        host = Controller.args.host
    if Controller.args.dport is None:
        port = 514
    else:
        port = int(Controller.args.dport)
    if Controller.args.count is None:
        count = 1
    else:
        count = int(Controller.args.count)
    run(host, port, data, count)



if "__main__" == __name__:
    # 初始化控制类对象：实例化浏览器实例
    Controller.init()
    senddata()
    # if Controller.args.thread is None:
    #     thread = 1
    # else:
    #     thread = int(Controller.args.thread)
    # tlst = []
    #
    # for i in xrange(thread):
    #     th = threading.Thread(senddata())
    #     tlst.append(th)
    #
    # for i in tlst:
    #     i.start()