__author__ = 'ray'

import random
import socket
import struct
import ConfigParser

# cf = ConfigParser.ConfigParser()
# cf.read('send.config')
# ip = cf.get('ipnet', 'ip')
#
# RANDOM_IP_POOL=['10.0.1.10/24']
def get_random_ip(RANDOM_IP_POOL):
    str_ip = RANDOM_IP_POOL[random.randint(0, len(RANDOM_IP_POOL) - 1)]
    # print str_ip
    str_ip_addr = str_ip.split('/')[0]
    # print str_ip_addr
    str_ip_mask = str_ip.split('/')[1]
    # print str_ip_mask
    ip_addr = struct.unpack('>I', socket.inet_aton(str_ip_addr))[0]
    mask = 0x0
    for i in range(31, 31 - int(str_ip_mask), -1):
        mask = mask | ( 1 << i)
    ip_addr_min = ip_addr & (mask & 0xffffffff)
    ip_addr_max = ip_addr | (~mask & 0xffffffff)
    # print socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))
    return socket.inet_ntoa(struct.pack('>I', random.randint(ip_addr_min, ip_addr_max)))

def get_random_mac():
    maclist = []
    for i in xrange(6):
        randstr = "".join(random.sample('0123456789abcdef',2))
        maclist.append(randstr)
        randmac = ":".join(maclist)
    return randmac
if __name__ == '__main__':
    # __get_random_ip(RANDOM_IP_POOL)
    get_random_mac()