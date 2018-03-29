# -*- coding:utf-8 -*-
import re

import paramiko

__author__ = 'Ray'
from selenium import webdriver
import unittest
import time
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')

class Demo(unittest.TestCase):

    #脚本初始化
    def setUp(self):
        option = webdriver.ChromeOptions()
        option.add_argument('test-type')
        self.driver = webdriver.Chrome(chrome_options=option)
        self.driver.implicitly_wait(30)
        self.base_url = "https://192.168.110.114/login"
        self.username = 'root'
        self.password = 'root12345'
        self.verifycode = '@c0rnC0d$'

    #测试用例
    def test_mwupgrade(self):
        """
        mwupgrade script
        """
        driver = self.driver
        print ur"========【MW在线升级程序】============="

        print ur"获取升级文件"
        mwupgrade = self.get_bin()
        if mwupgrade is not None:
            driver.get(self.base_url + "/")
            driver.maximize_window()
            print ur"进行登录"
            driver.find_element_by_id("login_text_username").clear()
            driver.find_element_by_id("login_text_username").send_keys(self.username)
            driver.find_element_by_id("login_text_password").clear()
            driver.find_element_by_id("login_text_password").send_keys(self.password)
            driver.find_element_by_id("login_text_verifycode").clear()
            driver.find_element_by_id("login_text_verifycode").send_keys(self.verifycode)
            driver.find_element_by_id("login_button_loginButton").click()

            time.sleep(2)
            #点击系统重置
            driver.find_element_by_css_selector("#setting-systemconsole_li_systemReset a").click()
            time.sleep(1)
            #点击恢复出厂
            driver.find_element_by_css_selector("#setting-systemconsole_button_resetModal").click()
            time.sleep(2)
            #点击确定
            driver.find_element_by_css_selector(".modal-content button:nth-child(2)").click()
            #等待160秒
            print "重置中请稍等..."
            for j in xrange(15):
                for i in xrange(20):
                    time.sleep(1)
                    print '.',
                print "."
            #点击开始升级

            print ur"重置完成，重新登录进行升级"
            driver.get(self.base_url + "/")
            driver.find_element_by_id("login_text_username").clear()
            driver.find_element_by_id("login_text_username").send_keys(self.username)
            driver.find_element_by_id("login_text_password").clear()
            driver.find_element_by_id("login_text_password").send_keys(self.password)
            driver.find_element_by_id("login_text_verifycode").clear()
            driver.find_element_by_id("login_text_verifycode").send_keys(self.verifycode)
            driver.find_element_by_id("login_button_loginButton").click()
            time.sleep(2)
            #点击系统设置
            driver.find_element_by_css_selector("#header_li_setting a").click()
            print "点击系统升级"
            #点击系统升级
            time.sleep(1)
            driver.find_element_by_css_selector("#setting-systemconsole_li_systemUpgrade a").click()
            time.sleep(1)
            #上传升级文件
            print ur"上传升级文件"
            driver.find_element_by_css_selector(ur"#setting-systemconsole_li_systemUpgrade_browse>input").send_keys(mwupgrade)
            #等待180秒
            for j in xrange(8):
                for i in xrange(20):
                    time.sleep(1)
                    print '.',
                print "."
            #点击开始升级
            print u"点击开始升级"
            driver.find_element_by_css_selector("#setting-systemconsole_li_systemUpgrade_start").click()
            time.sleep(3)
            #点击确认升级
            print u"点击确认升级"
            driver.find_element_by_xpath("//button[@ng-click='done()']").click()
            #等待160秒
            print ur"开始升级,并重启服务"
            for j in xrange(15):
                for i in xrange(20):
                    time.sleep(1)
                    print '.',
                print "."
            url = driver.current_url
            hostname = re.search('\d+\.\d+\.\d+\.\d+', url).group(0)
            port = 22
            username = 'acorn'
            password = 'Ag0@dbegiNNingmakesag0@dending.'

            try:
                paramiko.util.log_to_file("paramiko.log")
                s = paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(hostname=hostname, port=port, username=username, password=password)

                tt = s.invoke_shell()
                tt.send('sudo reboot')
                tt.send('\n')
                tt.send(password)
                tt.send('\n')
                while not tt.recv_ready():
                    print "working..."
                    time.sleep(10)
                print tt.recv(1024)
                s.close()
            except:
                print  u"MW 连接失败"
            print ur"重新登录,验证版本"
            driver.get(self.base_url + "/")
            time.sleep(3)
            driver.find_element_by_id("login_text_username").clear()
            driver.find_element_by_id("login_text_username").send_keys(self.username)
            driver.find_element_by_id("login_text_password").clear()
            driver.find_element_by_id("login_text_password").send_keys(self.password)
            driver.find_element_by_id("login_text_verifycode").clear()
            driver.find_element_by_id("login_text_verifycode").send_keys(self.verifycode)
            driver.find_element_by_id("login_button_loginButton").click()
            #等待1秒
            time.sleep(1)
            print ur"检查系统当前验证版本"
            #点击系统设置
            driver.find_element_by_css_selector("#header_li_setting a").click()
            #点击系统升级
            driver.find_element_by_css_selector("#setting-systemconsole_li_systemUpgrade a").click()
            time.sleep(1)

            #获取当前版本号
            mc_version_text = driver.find_element_by_xpath(u"//div[contains(text(),'当前系统版本号')]").text
            #进行版本校验
            print mc_version_text
            print ur"升级包:"+mwupgrade
            mwupgradetext = mc_version_text[mc_version_text.find('MC'):mc_version_text.find('-C0')]
            if mwupgradetext in mwupgrade:
                print ur"版本一致升级成功！ 进行版本测试。"
                self.driver.quit()
                os.system("python TestSuite.py -t 1 -u tsbc -r 1433")
            else:
                print ur"版本不一致升级失败！"
                self.driver.quit()
        else:
            print ur"升级文件不存在，升级失败"
            self.driver.quit()

    #脚本退出
    def tearDown(self):
        pass

    def get_bin(self):
        current_path = os.path.split(os.path.realpath(__file__))[0]
        for item in os.listdir(current_path):
            if os.path.splitext(item)[1].upper() == '.BIN':
                return os.path.realpath(item)
        return None

if __name__ == "__main__":
    unittest.main()
