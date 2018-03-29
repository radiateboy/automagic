# -*-coding:utf-8-*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2016-09-03
"""
from RestApiUtil import call_get, call_post


def sendFlowData(simulatorIP, testServerIP, type):
    url_post = "http://"+simulatorIP+"/api/v1/kafka/send/flowdata"
    para_dict = {"mw_ip": testServerIP}
    if "modbus" == type:
        para_dict["filename"] = "modbus.flowData2"
    elif "all" == type:
        para_dict["filename"] = "all.flowData2"

    call_post(url_post, para_dict)

def sendTrafoFlowData(simulatorIP, trafoServerIp, type, timeoutSeconds=None):
    url_post = "http://" + simulatorIP + "/api/v1/trafo/run"
    para_dict = {}
    para_dict = {"trafo_ip": trafoServerIp,
                 "trafo_usr": "test",
                 "trafo_passwd": "admin@123",
                 "debug_level": "1"}
    if timeoutSeconds is None:
        para_dict["timer"] = '120'
    else:
        para_dict["timer"] = timeoutSeconds
    confFileName = "eth1-2_58_" + type + ".json"
    para_dict["conf_file"] = confFileName
    call_post(url_post, para_dict)

def sendAuditFlowData(simulatorIP, testServerIP, type):
    url_post = "http://"+simulatorIP+"/api/v1/kafka/send/networkanalysis"
    para_dict = {}
    para_dict["dest_ip"] = testServerIP

    fileNameDict = {"telnet": "telnet.telnetAccountingData",
                    "http": "http.httpAccountingData",
                    "ftp": "ftp.ftpAccountingData",
                    "smtp": "smtp.smtpAccountingData",
                    "pop3": "pop3.pop3AccountingData"}
    para_dict["filename"] = fileNameDict[type]
    call_post(url_post, para_dict)

def sendEventAndIncident(simulatorIP, testServerIP, dpisn, type):
    url_post = ''
    para_dict = {"dest_ip": testServerIP,
                 "box_id": dpisn}
    if 'incident' == type:
        url_post = "http://" + simulatorIP + "/api/v1/kafka/send/incident"
        para_dict["filename"] = "whitelist.alert2"
    else:
        url_post = "http://" + simulatorIP + "/api/v1/kafka/send/boxevent"
        if "event1" == type:
            ports = [True, True, False, False]
        else:
            ports = [True, True, True, True]
        para_dict["ports"] = ports

    call_post(url_post, para_dict)

def generateDpiLog(simulatorIP, testServerIP, dpisn, type):
    url_post = ''
    para_dict = {"dest_ip": testServerIP,
                 "box_id": dpisn}

    if 'dpilogin' == type:
        url_post = "http://"+simulatorIP+"/api/v1/kafka/send/dpiuserlogin"
        para_dict["user_ip"] = "10.0.10.199"
        para_dict["reason"] = "DpiUserLogin Auto Test"
        para_dict["user"] = "Auto Tester"
        para_dict["result"] = 1
    elif 'dpicmdlog' == type:
        url_post = "http://" + simulatorIP + "/api/v1/kafka/send/dpicmdlog";
        para_dict["cmd"] = "DpiCmdLog Auto Test"
        para_dict["user_ip"] = "10.0.10.199"
        para_dict["user"] ="Auto Tester"
        para_dict["result"] = 0
    elif 'dpifwlog' == type:
        url_post = "http://" + simulatorIP + "/api/v1/kafka/send/dpifwlog"
        para_dict["reason"] = "DpiFwLog Auto Test"

    call_post(url_post, para_dict)

if '__main__' == __name__:
    #sendFlowData('127.0.0.1:4000', '192.168.1.135', 'all')
    for i in xrange(1):
        #sendEventAndIncident('192.168.116.3:4000', '172.18.51.111', 'ZB0202C400000092', 'incident')
        sendTrafoFlowData('192.168.110.77:4000', '192.168.110.77', 'dnp3', timeoutSeconds=None)
        # sendFlowData('192.168.116.3:4000', '192.168.110.114', 'modbus')
