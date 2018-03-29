# -*- coding: utf-8 -*-
__author__ = 'Ray'

"""
Python syslog 发包工具.
mail：tsbc@vip.qq.com
2016-05-05
"""

import socket
import threading
import ConfigParser
import random
import randomip
import weighted_choice
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class send:
    def __init__(self, message, host, port):
        self.message = message
        self.host = host
        self.port = port
        self.FACILITY = {
            'kern': 0, 'user': 1, 'mail': 2, 'daemon': 3,
            'auth': 4, 'syslog': 5, 'lpr': 6, 'news': 7,
            'uucp': 8, 'cron': 9, 'authpriv': 10, 'ftp': 11,
            'local0': 16, 'local1': 17, 'local2': 18, 'local3': 19,
            'local4': 20, 'local5': 21, 'local6': 22, 'local7': 23,
        }

        self.LEVEL = {
            'emerg': 0, 'alert':1, 'crit': 2, 'err': 3,
            'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
        }
        weights = [0.03, 0.04, 0.05, 0.07, 0.1, 0.2, 0.5, 0.01] #随机产生日志级别的概率

        if 'success' in self.message:
            self.levl = self.LEVEL['info']
        elif 'failed' in self.message:
            self.levl = self.LEVEL['warning']
        elif 'permit' in self.message:
            self.levl = self.LEVEL['info']
        elif 'deny' in self.message:
            self.levl = self.LEVEL['warning']
        else:
            self.levl = weighted_choice.weighted_choice_sub(weights)
            # self.levl = random.choice(self.LEVEL.keys())
    def run(self):

        """
        Send syslog UDP packet to given host and port.
        """
        BUFSIZE = 4096
        ADDR = (self.host,self.port)
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect(ADDR)
        except Exception,E:
            print "Connect Error",E
            return False

        data = '<%d>%s' % (self.levl + self.FACILITY['local7']*8, self.message)
        print data
        # sock.sendto(data, (self.host, self.port))
        while True:
            try:
                sock.send(data)
                data = sock.recv(BUFSIZE)
                if not data:
                    break
                print "Server:",data
            except Exception,e:
                print "Error",e
        sock.close()

if __name__ == '__main__':
    # 从配置文件读取数据
    cf = ConfigParser.ConfigParser()
    cf.read('send.config')
    host = cf.get('receiver', 'host').split(',')  # 获取接收log服务主机
    port = int(cf.get('receiver', 'port'))
    sip = randomip.get_random_ip([cf.get('mesg', 'sip')])  # 随机生成源IP
    dip = randomip.get_random_ip([cf.get('mesg', 'dip')])  # 随机生成目的IP
    sportstr = tuple(cf.get('mesg', 'sport').split(','))  # 随机生成源端口
    sport = str(random.randint(int(sportstr[0]), int(sportstr[1])))
    dportstr = cf.get('mesg', 'dport').split(',')  # 随机生成目的端口
    dport = random.choice(dportstr)

    # 获取系统当前时间
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    nowstr = time.strftime('%b %d %H:%M:%S', time.localtime())

    '''H3C交换机'''
    h3clog1 = nowstr + ' 2000 H3C %%10IFNET/3/LINK_UPDOWN(l): GigabitEthernet1/0/7 link status is UP.'
    h3clog2 = nowstr + ' 2000 H3C %%10SHELL/4/LOGOUT(t):   Trap 1.3.6.1.4.1.25506.2.2.1.1.3.0.2<hh3cLogOut>: logout from VTY'
    threadh3c1 = send(h3clog1, host[0], port)
    threadh3c2 = send(h3clog2, host[0], port)

    '''Cisco路由器'''
    # 管理员操作
    csicolog1 = '29: *' + nowstr + '.' + str(
        random.randint(001, 999)) + ': %SYS-5-CONFIG_I: Configured from console by admin on vty0 (10.0.1.49)'
    print csicolog1
    threadcisco1 = send(csicolog1, host[0], port)

    threadcisco1.run()