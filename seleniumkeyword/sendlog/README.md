#流量回放模式(Linux)

##通过回放Syslog流进行发送syslog(UDP支持源地址伪装)|sendingdata.py

**usage:**</br>
sendingdata.py [-h] [-sip SRCIP] [-dip DSTIP] [-p PROTOCOL] [-dport DPORT]</br> [-c COUNT] [-f FILE] [-t THREAD] [-s SPEED]

**optional arguments:**</br>
-h, --help    show this help message</br>
-sip SRCIP    src ip addr</br>
-dip DSTIP    dst ip addr</br>
-p PROTOCOL   protocol udp or tcp</br>
-dport DPORT  send port</br>
-c COUNT      packets count</br>
-f FILE       packets file</br>
-t THREAD     thread number</br>
-s SPEED      send speed (s)</br>

#UDP Socket
##通过UDP Socket发送syslog事件|udpsendingsyslog.py
**Usge:**</br>
python sendlog -f [filepath] -c [cycles] -t [sleep time]
-d [Receiver Host] -p [Receiver port]

**Details:**</br>
-C    [开启无限循环]</br>
-f    [指派日志文件路径]</br>
-c    [指定循环次数]</br>
-t    [指定日志发送间隔时间 单位:秒]</br>
-d    [指定日志接收IP地址]</br>
-p    [指定日志接收端口（整数）]</br>
-v    [查看工具版本]</br>
-h    [查看帮助]</br>

#TCP Socket
##通过TCP Socket发送syslog事件|tcpsendingsyslog.py
**usage:**</br>
tcpsendingsyslog.py [-h] [-host HOST] [-port DPORT] [-c COUNT]</br>

**optional arguments:**</br>
  -h, --help   show this help message and exit</br>
  -host HOST   receive host ip</br>
  -port DPORT  send port</br>
  -c COUNT     count number</br>
