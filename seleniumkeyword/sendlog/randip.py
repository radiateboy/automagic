# -*- coding:utf-8 -*-


__author__ = 'Ray'

import random
import struct
from scapy.all import *
from scapy.layers.inet import IP, UDP

SOURCE = ['.'.join((str(random.randint(1, 254)) for _ in range(4))) for _ in range(100)]

print SOURCE[1]
data = struct.pack('=BHI', 0x12, 20, 1000)
pkt = IP(src=SOURCE[1], dst='192.168.110.178') / UDP(sport=12345, dport=514) / data
send(pkt, inter=1, count=5)
