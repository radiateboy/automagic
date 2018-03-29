# -*- coding: utf-8 -*-
__author__ = 'Ray'

"""
socket tcp send 发包工具.
mail：tsbc@vip.qq.com
2017-04-01
"""

import socket,time

address = ('192.168.110.158', 1470)
data = '''<188> 2017-02-27 17:29:30 SECURITY VUL host tsbc type desc "jiangpeng.chen@acorn-net.com" '''
for i in xrange(100):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect_ex(address)
    print s.getsockname()
    print s.getpeername()
    s.sendall(data+"["+str(1)+"]")
    # print s.recv(1024)
    time.sleep(1)
    s.close()
