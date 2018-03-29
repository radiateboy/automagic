# -*- coding: utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2017-02-27
"""

from scapy.all import *
from scapy.layers.inet import IP,UDP,TCP
import threading
import argparse

srcip = '192.168.110.249'
dstip = '192.168.110.234'
data = '''<188> 2017-02-27 17:29:30 SECURITY VUL host tsbc type 常规  mintype 轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击"'''
# pkt = IP(src=srcip, dst=dstip)/UDP(sport=12345,dport=514)/data
# send(pkt,count=80000)
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
    parser.add_argument('-sip', action='store', dest='srcip', type=str, help='src ip addr')
    parser.add_argument('-dip', action='store', dest='dstip', type=str, help='dst ip addr')
    parser.add_argument('-p', action='store', dest='protocol', type=str, help='protocol udp or tcp')
    parser.add_argument('-dport', action='store', dest='dport', type=str, help='send port')
    parser.add_argument('-c', action='store', dest='count', type=str, help='packets count')
    parser.add_argument('-f', action='store', dest='file', type=str, help='packets file')
    parser.add_argument('-t', action='store', dest='thread', type=str, help='thread number')
    parser.add_argument('-s', action='store', dest='speed', type=str, help='send speed (s)')
    rst = parser.parse_args()
    return rst

def run(srcip, dstip,data,protocol,dport,count,speed):

    if protocol.upper() == 'UDP':
        pkt = IP(src=srcip, dst=dstip)/UDP(sport=12345,dport=dport)/data
        send(pkt,inter=speed, count=count)
    if protocol.upper() == 'TCP':
        pkt = IP(src=srcip, dst=dstip)/TCP(sport=12345, dport=dport) / data
        send(pkt, inter=speed, count=count)

def sendpkgdata():
    srcip = Controller.args.srcip
    dstip = Controller.args.dstip
    data = '''<188> 2017-02-27 17:29:30 SECURITY VUL host tsbc type 常规  mintype 轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击"'''
    if Controller.args.protocol is None:
        protocol = 'udp'
    else:
        protocol = Controller.args.protocol
    if Controller.args.dport is None:
        dport = 514
    else:
        dport = Controller.args.dport
    if Controller.args.count is None:
        count = 1
    else:
        count = int(Controller.args.count)
    if Controller.args.speed is None:
        speed = 0
    else:
        speed = float(Controller.args.speed)
    run(srcip, dstip, data, protocol, dport, count, speed)



if "__main__" == __name__:
    # 初始化控制类对象：实例化浏览器实例
    Controller.init()
    if Controller.args.thread is None:
        thread = 1
    else:
        thread = int(Controller.args.thread)
    tlst = []

    for i in xrange(thread):
        th = threading.Thread(sendpkgdata())
        tlst.append(th)

    for i in tlst:
        i.start()