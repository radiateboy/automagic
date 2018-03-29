# -*- coding: utf-8 -*-
__author__ = 'Ray'

"""
Sending Tools
mail：tsbc@vip.qq.com
2016-06-13
"""
import socket
import threading
import ConfigParser
import random
import randomip
import weighted_choice
import sys, time, os, getopt
reload(sys)
sys.setdefaultencoding('utf-8')

class sending(threading.Thread):
    """send log"""
    def __init__(self):
        threading.Thread.__init__(self)
        self.thread_stop = False
        try:
            self.opts, self.args = getopt.getopt(sys.argv[1:], "hvCf:c:t:d:p:")
        except:
            print u"命令语法错误，可使用 -h 查看帮助。"
            sys.exit()
        cf = ConfigParser.ConfigParser()
        cf.read('send.config')
        self.host = cf.get('receiver', 'host').split(',')
        self.port = int(cf.get('receiver', 'port'))
        self.sip = randomip.get_random_ip([cf.get('mesg', 'sip')])#随机生成源IP
        self.dip = randomip.get_random_ip([cf.get('mesg', 'dip')])#随机生成目的IP
        self.sportstr = tuple(cf.get('mesg', 'sport').split(',')) #随机生成源端口
        self.sport = str(random.randint(int(self.sportstr[0]), int(self.sportstr[1])))
        self.dportstr = cf.get('mesg', 'dport').split(',')#随机生成目的端口
        self.dport = random.choice(self.dportstr)

        #获取系统当前时间
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        nowstr = time.strftime('%b %d %H:%M:%S', time.localtime())

        #syslog日志类型
        self.FACILITY = {
            'kern': 0, 'user': 1, 'mail': 2, 'daemon': 3,
            'auth': 4, 'syslog': 5, 'lpr': 6, 'news': 7,
            'uucp': 8, 'cron': 9, 'authpriv': 10, 'ftp': 11,
            'local0': 16, 'local1': 17, 'local2': 18, 'local3': 19,
            'local4': 20, 'local5': 21, 'local6': 22, 'local7': 23,
        }

        #syslog日志级别
        self.LEVEL = {
            'emerg': 0, 'alert':1, 'crit': 2, 'err': 3,
            'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
        }
        weights = [0.03, 0.04, 0.05, 0.07, 0.1, 0.2, 0.5, 0.01] #随机产生日志级别的概率
        self.message = []

        '''漏扫'''
        #操作日志
        nvaslog1 = ' '+now + u' ADMIN CONFIG user admin ip 10.0.1.48 module 系统-云中心配置 cmd "云中心配置。" result '+random.choice(['success', 'failed'])
        self.message.append(nvaslog1)
        #管理员登录
        nvaslog2 = ' '+now + u' ADMIN LOGIN user tsbc ip 10.0.1.104 action login result '+random.choice(['success', 'failed'])
        self.message.append(nvaslog2)
        #漏洞发现
        nvaslog3 = ' '+now + u' SECURITY VUL host tsbc type 常规  mintype 轻蠕虫 id CN-CVE name 洪泛攻击 desc "容易受到ARP攻击"'
        self.message.append(nvaslog3)

        '''信息审计'''
        #内容审计
        bca1 = ' '+now + u' AUDIT CONTENT user admin usergroup 管理员组 access permit prot tcp sip ' + self.sip + ' sport ' + self.sport + ' dip ' + self.dip + u' dport 80 type HTTP url http://www.163.com filename "找工作.txt" keyword 找工作 cmd "找工作" subject 邮件主题 sender lietou@163.com receiver lietou@163.com'
        self.message.append(bca1)
        bca2 = ' '+now + u' AUDIT CONTENT user admin usergroup 管理员组 access deny prot tcp sip ' + self.sip + ' sport ' + self.sport + ' dip ' + self.dip + u' dport 80 type HTTP url http://mail.163.com filename "找工作.txt" keyword 找工作 cmd "找工作" subject 邮件主题 sender lietou@163.com receiver lietou@163.com'
        self.message.append(bca2)
        #应用行为审计
        bca3 = ' '+now + ' AUDIT APP user 10.0.1.48 usergroup NULL access permit prot "UDP" sip ' + self.sip + ' sport ' + self.sport + ' dip ' + self.dip + ' dport ' + self.dport + u' type "IM通信" behav "飞秋" desc "内置特征"'
        self.message.append(bca3)

        '''上网行为'''
        #IP访问事件  --事件入库了但是界面没有对应的类别查询不到
        nca1 = ' '+now + ' SECURITY POLICY access permit prot http smac 00:22:46:0D:91:7C dmac 00:22:46:0D:91:7C sip ' + self.sip + ' sport ' + self.sport + ' dip ' + self.dip + ' dport ' + self.dport + ' times 1'
        self.message.append(nca1)
        #应用行为审计
        nca2 = ' '+now + u' AUDIT APP user tsbc usergroup 管理员组 access deny prot 代理上网 sip ' + self.sip + ' sport ' + self.sport + ' dip ' + self.dip + ' dport ' + self.dport + u' type GAME behav 访问网络游戏 desc "访问英雄联盟游戏"'
        self.message.append(nca2)
        #用户认证事件
        nca3 = ' '+now + u' USER AUTH name tsbc group 管理员组 ip ' + self.sip + ' type local result '+random.choice(['success', 'failed'])
        self.message.append(nca3)

        '''IDS/IPS'''
        #设备流量日志
        idslog1 = ' '+now + ' SYSTEM TRAFFIC sendbps 10211 recvbps 10211 sendpps 19621 recvpps 18954'
        self.message.append(idslog1)

        '''Jump防火墙'''
        #安全监测/访问控制
        fwlog1 = ' '+now + ' SECURITY POLICY access permit prot TCP smac 00:22:46:1d:eb:b5 dmac 00:22:46:1f:aa:47 sip ' + self.sip + ' sport ' + self.sport + ' dip ' + self.dip + ' dport ' + self.dport + ' times 1'
        self.message.append(fwlog1)
        #攻击检测
        fwlog2 = ' '+now + ' SECURITY INSTRUCTION type ddos id '+str(random.randint(1000, 9999))+ u' name "尝试攻击" smac 00:22:46:0D:91:7d  dmac 00:22:46:0D:91:7C prot ICMP sip ' + self.sip + ' sport ' + self.sport + ' dip ' + self.dip + ' dport ' + self.dport + ' times 1'
        self.message.append(fwlog2)
        #病毒日志
        fwlog3 = ' '+now + u' SECURITY VIRUS type 木马病毒 name "灰鸽子" smac 00:22:46:0A:B1:BC  dmac 00:22:46:0D:91:7C prot tcp sip ' + self.sip + ' sport ' + self.sport + ' dip ' + self.dip + ' dport ' + self.dport + u' filename "新建文本文档.exe"'
        self.message.append(fwlog3)
        #隧道日志
        fwlog4 = ' '+now + ' IPSEC TUNNEL id 1 localip ' + self.sip + ' remote ' + self.dip + ' desc "Error!!!"'
        self.message.append(fwlog4)

        '''主机审计'''
        #移动介质审计
        hostlog1 = ' '+now + u' AUDIT MEDIUM operator admin action 接入 medtype U 盘 medname 小明的U盘 access "D:\Menu" times 50 result '+random.choice(['permit', 'deny'])
        self.message.append(hostlog1)

        '''用户/系统'''
        #网口状态变化
        systemlog1 = ' '+now + ' SYSTEM INTERFACE eth '+str(random.randint(0, 10))+' type '+random.choice(['phy', 'link'])+' state '+random.choice(['up', 'down'])
        self.message.append(systemlog1)
        #用户登录
        systemlog2 = ' '+now + u' USER LOGIN user tsbc group 运维管理员组 ip '+ self.dip +' action '+random.choice(['login', 'logout'])+' result '+random.choice(['success', 'failed'])
        self.message.append(systemlog2)
        #用户认证
        systemlog3 = ' '+now + u' USER AUTH name tsbc group 运维管理员组 ip '+ self.dip +' type '+random.choice(['local', 'radius', 'tacacs', 'ldap', 'msad', 'pop3', 'cert', 'other'])+' result '+random.choice(['success', 'failed'])
        self.message.append(systemlog3)
        #用户访问资源
        systemlog4 = ' '+now + u' USER ACCESS name tsbc group 安全管理员组 restype web resname "信息审计系统" sip '+ self.sip +' dip '+ self.dip +' prot tcp sport '+ self.sport +' dport '+ self.dport +' result '+random.choice(['permit', 'deny'])
        self.message.append(systemlog4)
        #性能日志
        systemlog5 = ' '+now + ' SYSTEM PERFORMANCE cpu '+str(random.randint(80, 90))+' memory '+str(random.randint(75, 95))+' connections '+str(random.randint(80, 300))
        self.message.append(systemlog5)
        #系统关键进程
        systemlog6 = ' '+now + ' SYSTEM PROCESS explorer.exe exit'
        self.message.append(systemlog6)

        '''H3C交换机'''
        h3clog1 = nowstr + ' 2000 H3C %%10IFNET/3/LINK_UPDOWN(l): GigabitEthernet1/0/7 link status is UP.'
        self.message.append(h3clog1)
        h3clog2 = nowstr + ' 2000 H3C %%10SHELL/4/LOGOUT(t):   Trap 1.3.6.1.4.1.25506.2.2.1.1.3.0.2<hh3cLogOut>: logout from VTY'
        self.message.append(h3clog2)

        '''Cisco路由器'''
        #管理员操作
        csicolog1 = '29: *'+nowstr+'.'+ str(random.randint(001, 999)) +': %SYS-5-CONFIG_I: Configured from console by admin on vty0 (10.0.1.49)'
        self.message.append(csicolog1)


        if self.message is not os.path:
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

        self.input_file = ''
        self.count = 1
        #self.host = self.host
        self.port = 514
        self.n = .0
        self.x = False
        self.fx = True
        for op, value in self.opts:
            if op == '-f':
                self.input_file = value
                self.fx = False
            if op == '-v':
                print "SendingTools Version 1.0"
                sys.exit()
            elif op == "-c":
                try:
                    self.count = int(value)
                except:
                    print u'-c 参数值错误, 可使用 -h 查看帮助。'
                    sys.exit()
            elif op == "-C":
                self.x = True
            elif op == "-d":
                self.host = []
                self.host.append(value)
            elif op == "-p":
                try:
                    self.port = int(value)
                except:
                    print u'-p 参数值错误, 可使用 -h 查看帮助。'
                    sys.exit()
            elif op == "-t":
                try:
                    self.n = float(value)
                except:
                    print u'-t 参数值错误, 可使用 -h 查看帮助。'
                    sys.exit()
            elif op == "-h" or op =="-help":
                self.usage()
                sys.exit()
    def usage(self):
        """帮助文档"""
        print u"""            This is a Sending log Tools:
-------------------------------------------------------------------------------------------
    Usge:
        python sendlog -f [filepath] -c [cycles] -t [sleep time]
            -d [Receiver Host] -p [Receiver port]
    Details:
    -C    Cycle send log                [开启无限循环]
    -f    Specify the path to log file         [指派日志文件路径]
    -c    Specify number of cycles         [指定循环次数]
    -t    Specify log sending time interval     [指定日志发送间隔时间 单位:秒]
    -d    Specify Receive log IP Addr         [指定日志接收IP地址]
    -p    Specify Receive log Dst Prot         [指定日志接收端口（整数）]
    -v    Show version                 [查看工具版本]
    -h    Show help info                 [查看帮助]"""

    def run(self):
        """
        Send syslog UDP packet to given host and port.
        """

        if self.fx:#fx为True 发送脚本样例
            if self.x: #传入 -C 参数进行无限循环
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while True:
                    time.sleep(float(self.n))
                    for h in self.host:
                        for i in xrange(0, self.count):
                            for msg in self.message:
                                data = '<%d>%s' % (self.levl + self.FACILITY['local7']*8, msg)
                                time.sleep(self.n)
                                try:
                                    sock.sendto(data, (h, self.port))
                                    print data
                                except:
                                    print u"参数取值出现错误，使用 -h 查看帮助。"
                                    sys.exit()
                sock.close()
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                for h in self.host:
                    #print h
                    for i in xrange(0, self.count):
                        for msg in self.message:
                            data = '<%d>%s' % (self.levl + self.FACILITY['local7']*8, msg)
                            time.sleep(self.n)
                            #print self.n
                            try:
                                sock.sendto(data, (h, self.port))
                                print data
                            except:
                                print u"参数取值出现错误，使用 -h 查看帮助。"
                                sys.exit()
                sock.close()
        else:#-f 读取日志文件
            if self.x:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                while True:
                    for i in xrange(0, self.count):
                        try:
                            f = open(self.input_file, 'r')
                            lines = f.readlines()
                        except IOError:
                            print u'读取的日志文件不存在，请更正后再试。'
                            sys.exit()
                        for line in lines:
                            time.sleep(self.n)
                            for h in self.host:
                                try:
                                    sock.sendto(line, (h, self.port))
                                    print line
                                except:
                                    print u"参数取值出现错误，使用 -h 查看帮助。"
                                    sys.exit()
                        f.close()
                sock.close()
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                for j in xrange(0, self.count):
                    try:
                        f = open(self.input_file, 'r')
                        lines = f.readlines()
                    except IOError:
                        print u'-f 文件路径不存在，可使用 -h 查看帮助。'
                        sys.exit()
                    for line in lines:
                        time.sleep(self.n)
                        for h in self.host:
                            try:
                                sock.sendto(line, (h, self.port))
                                print line
                            except:
                                print u"参数取值出现错误，使用 -h 查看帮助。"
                                sys.exit()
                    f.close()
                sock.close()
    def stop(self):
        self.thread_stop = True

def sendfile():
    thread1 = sending()
    thread1.start()
    thread1.stop()

if __name__ == '__main__':
    for i in xrange(1):
        # print i
        sendfile()