# -*- coding: utf-8 -*-

import time,datetime
import os,sys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import paramiko
import SimulatorUtil
import re

if sys.platform.startswith('win'):
        from sendlog import tcpsendingsyslog, udpsendingsyslog
else:
        from sendlog import sendingdata, tcpsendingsyslog, udpsendingsyslog

class Action(object):
        keyword2action = {}

        def __init__(self):
                # option = webdriver.ChromeOptions()
                # option.add_argument('test-type')
                # self.driver = webdriver.Chrome(chrome_options=option)
                # self.driver = webdriver.PhantomJS()
                self.driver = None

        def __del__(self):
                if self.driver is not None:
                        self.driver.quit()
                        self.driver = None

        @classmethod
        def add_action(cls, keyword):
                def deco(func):
                        def _deco(*args, **kwargs):
                                print args[1]
                                return func(*args, **kwargs)
                        cls.keyword2action[keyword] = _deco
                        return _deco
                return deco

        # 元素高亮显示
        def highlightElement(self, element):
                self.driver.execute_script("element = arguments[0];" +
                                                                   "original_style = element.getAttribute('style');" +
                                                                   "element.setAttribute('style', original_style + \";" +
                                                                   "background: #1874cd; border: 2px solid red;\");" +
                                                                   "setTimeout(function(){element.setAttribute('style', original_style);}, 1000);",
                                                                   element)
        #页面顶部加步骤输出
        def notes(self, text):
                js1 = u"""var bodyDom = document.getElementsByTagName('body')[0];
                var insertDiv = document.createElement('div');
                insertDiv.id = 'sdiv';
                insertDiv.style.backgroundColor = 'red';
                insertDiv.style.height = '20px';
                insertDiv.style.color = '#FFF';
                insertDiv.style.textalign = 'center';
                insertDiv.innerText = '"""
                js2 = u"""';
                var firstdiv = bodyDom.getElementsByTagName('div')[0];
                bodyDom.insertBefore(insertDiv,firstdiv);
                """
                js = js1 + text +js2
                self.driver.execute_script(js)

        #更新顶部note显示内容
        def show_note(self,stext):
                js = u"insertDiv = document.getElementById('sdiv');insertDiv.innerText ='"+stext+"';"
                self.save_runing_log(stext)
                self.driver.execute_script(js)

        # 重写定义send_keys方法
        def send_keys(self, loc, value):
                try:
                        self.find_element(loc).clear()
                except:
                        print u"%s 元素 %s 没有clear属性" % (self, loc)
                self.find_element(loc).send_keys(value)

        # 重写元素定位方法
        def find_element(self, loc):
                for i in xrange(3):
                        try:
                                # WebDriverWait(self.driver, 15).until(lambda driver: True if driver.find_element(*loc) is not None else False)
                                element = WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element(*loc))
                                # element = self.driver.find_element(*loc)
                                self.highlightElement(element)
                                return element
                        except:
                                pass
                # print u"%s 页面中未能找到 %s 元素" % (self, loc)

        # 重写一组元素定位方法
        def find_elements(self, loc):
                try:
                        elements = self.driver.find_elements(*loc)
                        if len(elements):
                                return elements
                except:
                        print u"%s 页面中未能找到 %s 元素" % (self, loc)

        #判断元素是否存在
        def isElementExsit(self, loc):
                try:
                        WebDriverWait(self.driver, 15).until(
                                lambda driver: True if driver.find_element(*loc) is not None else False)
                        # element = self.driver.find_element(*loc)
                        # self.highlightElement(element)
                        return True
                except:
                        return False

        # 定位一组元素中索引为第i个的元素 i从0开始
        def find_elements_i(self, index, loc):
                try:
                        elements = self.driver.find_elements(*loc)
                        if elements[index] is not None:
                                return elements[index]
                except:
                        print u"%s 页面中未能找到%s的第 %s 个元素 " % (self, loc, index)

        # saveScreenshot:通过图片名称，进行截图保存
        def saveScreenshot(self, name):
                """
                快照截图
                name:图片名称
                """
                image = self.driver.save_screenshot(self.savePngName(name))
                return image

        # 生成图片的名称
        def savePngName(self, name):
                """
                name：自定义图片的名称
                """
                day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                fp = "result/" + day + "/image"
                tm = self.saveTime()
                file_type = ".png"
                # 判断存放截图的目录是否存在，如果存在打印并返回目录名称，如果不存在，创建该目录后，再返回目录名称
                if os.path.exists(fp):
                        filename = str(fp) + "/" + str(tm) + str("_") + str(name) + str(file_type)
                        print filename
                        return filename
                else:
                        os.makedirs(fp)
                        filename = str(fp) + "/" + str(tm) + str("_") + str(name) + str(file_type)
                        print filename
                        return filename

        #生成log
        def save_runing_log(self, text):
                """
                :param text:
                :return:
                """
                day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                running_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                file_type = "running.log"
                fp = "result/" + day
                if os.path.exists(fp):
                        filename = str(fp) + "/" + str(file_type)
                        with open(filename,"a") as f:
                                f.write(running_time + "  " + text + '\n')
                        # os.system("echo " + running_time + "  " + text + ">> " + filename)
                else:
                        os.makedirs(fp)
                        filename = str(fp) + "/" + str(file_type)
                        # os.system("echo " + running_time + "  "  + text + ">> " + filename)
                        with open(filename,"a") as f:
                                f.write(running_time + "  " + text + '\n')

        # 生成图片的名称
        def saveVideoName(self, name):
                """
                name：自定义图片的名称
                """
                day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                fp = "result/" + day + "/image"
                tm = self.saveTime()
                file_type = ".ogv"
                # 判断存放截图的目录是否存在，如果存在打印并返回目录名称，如果不存在，创建该目录后，再返回目录名称
                if os.path.exists(fp):
                        filename = str(fp) + "/" + str(tm) + str("_") + str(name) + str(file_type)
                        print filename
                        return filename
                else:
                        os.makedirs(fp)
                        filename = str(fp) + "/" + str(tm) + str("_") + str(name) + str(file_type)
                        print filename
                        return filename

        # 获取系统当前时间
        def saveTime(self):
                """
                返回当前系统时间以括号中（2014-08-29-15_21_55）展示
                """
                return time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))

################################################################################
# 关键字函数必须用Aciton.add_action(keyword)装饰起进行装饰
# 函数的形参必须为4个:action_object(Aciton对象), step_desc(步骤描述信息，可用于记录log),
#                                  value(需要输入的值，多个输入值用逗号隔开), loc(元素的定位信息)
# 函数正常退出时不能有返回值（使用默认的返回值None），出错时返回字符串（记录出错信息）
################################################################################

@Action.add_action('openBrowser')
def action_openBrowser(action_object, step_desc, value, loc):
        """
        openBrowser 通过传参选择启动浏览器
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return:
        """
        # if action_object[0].driver is None:
        option = webdriver.ChromeOptions()
        downloaddir = os.path.abspath(os.curdir)+"/data"
        prefs = {"download.default_directory":downloaddir}
        option.add_experimental_option("prefs",prefs)
        option.add_argument('--no-sandbox')
        # action_object.driver = webdriver.Chrome(chrome_options=option)

        browser = value #传入浏览器对象
        if action_object.driver == None:
                if browser.upper() == 'IE': action_object.driver = webdriver.Ie()
                elif browser.upper() == 'CHROME': action_object.driver = webdriver.Chrome(chrome_options=option)
                elif browser.upper() == 'FIREFOX': action_object.driver = webdriver.Firefox()
                elif browser.upper() == 'SAFARI': action_object.driver = webdriver.Safari()
                elif browser.upper() == 'NW':
                        chromedriver = os.path.abspath(os.curdir)+"\\nwjs-sdk-v0.19.3-win-x64\\chromedriver.exe"
                        action_object.driver = webdriver.Chrome(chromedriver, chrome_options=option)
                        js = "var gui=require(\"nw.gui\"); var win=gui.Window.get(); win.maximize()"
                        action_object.driver.execute_script(js)
                else: action_object.driver = webdriver.Chrome(chrome_options=option)
                if browser.upper() != 'NW':
                        action_object.driver.set_window_size(1600, 900)
                        action_object.driver.maximize_window()

@Action.add_action('InputText')
def action_InputText(action_object, step_desc, value, loc):
        """
        文本框输入内容
        :param action_object:
        :param step_desc:
        :param value: text
        :param loc:
        :return:
        """
        print loc, value
        textinput = value
        if 'now+' in value:
                now_str = value.split('+')
                num = int(now_str[1])
                textinput = (datetime.datetime.now()+datetime.timedelta(minutes=num)).strftime('%Y-%m-%d %H:%M:%S')
        elif 'now-' in value:
                now_str = value.split('-')
                num = int(now_str[1])
                textinput = (datetime.datetime.now() + datetime.timedelta(minutes=-num)).strftime('%Y-%m-%d %H:%M:%S')
        elif value.lower() == 'now':
                textinput = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        action_object.send_keys(loc, textinput)

@Action.add_action('uploadfile')
def action_uploadfile(action_object, step_desc, value, loc):
        """
        上传文件
        :param action_object:
        :param step_desc:
        :param value:filename
        :param loc:
        :return:
        """
        current_path = os.path.split(os.path.realpath(__file__))[0]
        print loc, current_path+'/data/'+value
        action_object.send_keys(loc, current_path+'/data/'+value)

@Action.add_action('jscript')
def action_jscript(action_object, step_desc, value, loc):
        """
        执行javaScript
        :param action_object:
        :param step_desc:
        :param value:
        :param loc: javascript
        :return:
        """
        print value
        try:
                action_object.driver.execute_script(value)
        except Exception,e:
                return str(e)

@Action.add_action('moveScroll')
def action_moveScroll(action_object, step_desc, value, loc):
        """
        移动滚动条到某一元素位置（垂直）
        :param action_object:
        :param step_desc:
        :param value:
        :param loc: 目标元素
        :return:
        """
        print loc, value
        try:
                element = action_object.find_element(loc)
                action_object.driver.execute_script("arguments[0].scrollIntoView();", element)
        except Exception,e:
                return str(e)

@Action.add_action('scrollIntoView')
def action_moveScroll(action_object, step_desc, value, loc):
        """
        移动到某元素的位置
        :param action_object:
        :param step_desc:
        :param value:
        :param loc: 目标元素
        :return:
        """
        print loc, value
        try:
                element = action_object.find_element(loc)
                ActionChains(action_object.driver).move_to_element(element).perform()
        except Exception,e:
                return str(e)

@Action.add_action('timestamp')
def action_timestamp(action_object, step_desc, value, loc):
        """
        时间戳 输入当前时间戳
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return:
        """
        print loc, value
        t = time.time()  # 获取当前时间戳
        b = str(t).split('.')
        c = b[0]
        # print type(value), type(c)
        # if type(value) is float:
        #         f = str(value).split('.')
        #         txt = f[0] + c
        # else:
        #         txt = value + c
        # print loc, txt
        action_object.send_keys(loc, c)


@Action.add_action('submit')
def action_submit(action_object, step_desc, value, loc):
        """
        表单提交
        :param action_object:
        :param step_desc:
        :param value:
        :param loc: from location
        :return:
        """
        print loc, value
        action_object.saveScreenshot("submit")
        action_object.find_element(loc).click()

@Action.add_action('refresh')
def action_refresh(action_object, step_desc, value, loc):
        """
        时间戳 输入当前时间戳
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return:
        """
        action_object.driver.refresh()

@Action.add_action('closeBrowser')
def action_closeBrowser(action_object, step_desc, value, loc):
        """
        关闭浏览器
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return:
        """
        time.sleep(1)
        action_object.driver.quit()


@Action.add_action('navigate')
def action_navigate(action_object, step_desc, value, loc):
        """
        网页跳转
        :param action_object:
        :param step_desc:
        :param value: 跳转url  http://192.168.110.114/login,[title]
        :param loc:
        :return:
        """
        url = value
        pagetitle = None
        if ',' in value:
                url, pagetitle = value.strip().split(',')[:2]
        print url
        action_object.driver.get(url)
        try:
                action_object.notes(u'步骤走马灯')
        except:
                pass
        # 使用assert进行校验，打开的链接地址是否与配置的地址一致。调用on_page()方法
        if pagetitle is not None:
                assert pagetitle in action_object.driver.title, u"打开开页面失败 %s" % url


@Action.add_action('click')
def action_click(action_object, step_desc, value, loc):
        """
        点击一个元素
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return:
        """
        print loc, value
        action_object.find_element(loc).click()


@Action.add_action('clicks')
def action_clicks(action_object, step_desc, value, loc):
        """
        点击一组元素中的某一个元素
        :param action_object:
        :param step_desc:
        :param value: int 第几个从0开始
        :param loc: 一组元素
        :return:
        """
        print loc, value
        action_object.find_elements_i(int(value), loc).click()


@Action.add_action('checkclick')
def action_checkclick(action_object, step_desc, value, loc):
        """
        checkBox复选框循环全选
        :param action_object:
        :param step_desc:
        :param value:
        :param loc: 所有复选框对应的父级元素
        :return:
        """
        print loc, value
        if action_object.find_element(loc) is not None:
                aa = action_object.find_element(loc)
                for i in aa.find_elements_by_css_selector('input[type="checkbox"]'):
                        i.click()

@Action.add_action('select')
def action_select(action_object, step_desc, value,loc):
        """
        Option下拉框选择
        :param action_object:
        :param step_desc:
        :param value: 选择的框对应的value值
        :param loc: select元素
        :return:
        """
        print loc, value
        Select(action_object.find_element(loc)).select_by_value(value)

@Action.add_action('selectText')
def action_selectText(action_object, step_desc, value,loc):
        """
        Option下拉框选择
        :param action_object:
        :param step_desc:
        :param value: 选择菜单对应的Text文本内容
        :param loc: select元素
        :return:
        """
        print loc, value
        Select(action_object.find_element(loc)).select_by_visible_text(value)


@Action.add_action('swichframe')
def action_swichframe(action_object, step_desc, value, loc):
        """
        切换frame
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:要切换的frame元素
        :return:
        """
        print loc
        return action_object.driver.switch_to_frame(loc)


@Action.add_action('defaultframe')
def action_defaultframe(action_object, step_desc, value, loc):
        """
        进入默认frame
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return:
        """
        print loc, value
        action_object.driver.switch_to_default_content()


@Action.add_action('assert')
def action_assert(action_object, step_desc, value, loc):
        print loc, value
        expected = action_object.find_element(loc).text
        print u'预期结果：' + value
        print u'实际结果：' + expected
        if value not in expected:
                return u'实际结果和预期结果不同！'

@Action.add_action('ValueAssert')
def action_valueassert(action_object, step_desc, value, loc):
        """
        通过执行jQuery获取元素取值与另一元素取值进行对比
        :param action_object:
        :param step_desc:
        :param value:
        :param loc: element need css selector
        :return:jQuery('#login_text_username').val()
        """
        print loc, value
        expected = action_object.driver.execute_script("return jQuery('"+loc[1]+"').val()")
        print u'预期结果：' + value
        print u'实际结果：' + expected
        if value != expected:
                return u'实际结果和预期结果不同！'

@Action.add_action('Notassert')
def action_notassert(action_object, step_desc, value, loc):
        print loc, value
        elements = action_object.find_elements(loc)
        for i in elements:
                if value in i.text:
                        print u'预期结果：' + value
                        print u'实际结果：' + i.text
                        return u'实际结果和预期结果相同！'
        print u'预期结果：实际结果和预期结果不同！'

@Action.add_action('assertTrue')
def action_assertTrue(action_object, step_desc, value, loc):
        """
        断言界面元素是存在的
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return:
        """
        print loc
        print u'预期结果：元素存在'
        if action_object.isElementExsit(loc):
                print u'实际结果：元素存在'
        else:
                action_object.saveScreenshot("assertTrueError")
                return u'实际结果：元素不存在'


@Action.add_action('assertFalse')
def action_assertFalse(action_object, step_desc, value, loc):
        """
        断言界面元素是不存在的
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return: 元素不存在:true, 存在:false
        """
        print loc
        print u'预期结果：元素不存在'

        if action_object.isElementExsit(loc):
                action_object.saveScreenshot("assertTrueError")
                return u'实际结果：元素存在'
        else:
                print u'实际结果：元素不存在'

@Action.add_action('assertUrl')
def action_assertUrl(action_object, step_desc, value, loc):
        """
        验证URL是否正确
        :param action_object:
        :param step_desc:
        :param value:
        :param loc: 预期结果
        :return:
        """
        print value
        expected = action_object.driver.current_url
        print u'预期结果：' + value
        print u'实际结果：' + expected
        if value not in expected:
                action_object.saveScreenshot("urlError")
                return u'实际结果和预期结果不同！'


@Action.add_action('isDisplayed')
def action_isDisplayed(action_object, step_desc, value, loc):
        """
        验证元素是隐藏元素
        :param action_object:
        :param step_desc:
        :param value:
        :param loc: location
        :return: 隐藏为True,显示为 False
        """
        print loc
        print u'预期结果：元素是隐藏的',action_object.find_element(loc).is_displayed()
        if action_object.find_element(loc).is_displayed():
                return u'实际结果：元素是可见'
        else:
                print u'实际结果：元素是隐藏的'


@Action.add_action('isEnabled')
def action_isEnabled(action_object, step_desc, value, loc):
        """
        验证元素是否置灰
        :param action_object:
        :param step_desc:
        :param value:
        :param loc: location
        :return:
        """
        print loc
        print u'预期结果：元素是置灰的'
        not_active = "blurred" in action_object.find_element(loc).get_attribute("class")
        disabled = action_object.find_element(loc).get_attribute("disabled")
        print "active:",not_active,"-","disabled:",disabled

        if disabled is not None:
                print u'实际结果：元素是置灰的'
        elif not_active:
                print  u'实际结果：元素是置灰的'
        else:
                return u'实际结果：元素是可用的'


@Action.add_action('sleep')
def action_sleep(action_object, step_desc, value, loc):
        """
        强制脚本等待关键字
        :param action_object:
        :param step_desc:
        :param value: 等待时间单位是秒（s），float型
        :param loc:
        :return:
        """
        time.sleep(float(value))


@Action.add_action('ssh')
def sshclient_execmd(action_object, step_desc, value, loc):
        """
        通过ssh连接linux执行命令
        :param action_object:
        :param step_desc:
        :param value:[hostname,port,username,password,[command1;command2;command3;command4]]
        :param loc:
        :return:
        """
        print value
        hostname,port,username,password,execmd=value.split(',')
        paramiko.util.log_to_file("paramiko.log")
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=hostname, port=int(port), username=username, password=password)
        execmd = execmd.replace(";", ",")
        execmds = execmd.split(',')
        tt = s.invoke_shell()
        for i in execmds:
                tt.send(i)
                tt.send('\n')
                tt.send(' ')
                tt.send(' ')
                tt.send(' ')
                tt.send(' ')
        while not tt.recv_ready():
                time.sleep(5)
        print tt.recv(4096)
        s.close()

        # stdin, stdout, stderr = s.exec_command(execmd)
        # stdin.write("Y")
        # print stdout.read()
        # s.close()

@Action.add_action('exists_file')
def exists_file(action_object, step_desc, value, loc):
        """
        assert file exists
        :param action_object:
        :param step_desc:
        :param value:[filename],[file type]
        :param loc:
        :return:
        """
        current_path = os.path.split(os.path.realpath(__file__))[0]
        fname, ftype = value.split(',')
        day = time.strftime('%Y-%-m-%-d', time.localtime(time.time()))
        if ftype.lower() == 'pdf':
                pfname = fname + '_' + day + '.pdf'
        elif ftype.lower() == 'html':
                pfname = fname + '_' + day + '.html'
        else:
                pfname = fname + '.' + ftype.lower()
        print loc, current_path + '/data/' + pfname
        filename = current_path + '/data/' + pfname
        if os.path.exists(filename):
                print u"文件["+filename+u"]下载成功！"
        else:
                return u"文件下载失败！"

@Action.add_action('udpsend')
def action_udpsend(action_object,step_desc, value, loc):
        """
        调用sendlog中的脚本进行syslog发包
        :param action_object:
        :param step_desc:
        :param value:参数  -sip -dip -c -t...
        :param loc:
        :return:
        """

        if '-t' in value or '-sip' in value:
                print 'sudo python sendlog/sendingdata.py ' + str(value)
                try:
                        os.system('sudo python sendlog/sendingdata.py ' + str(value))
                except Exception,e:
                        print e
        if '-d ' in value:
                print 'sudo python sendlog/udpsendingsyslog.py ' + value
                try:
                        os.system('sudo python sendlog/udpsendingsyslog.py ' + str(value))
                except Exception,e:
                        print e

@Action.add_action('dpiblacklist')
def sshclient_dpiblacklist(action_object, step_desc, value, loc):
        """
        验证DPI端口映射下发
        :param action_object:
        :param step_desc:
        :param value:[hostname,port,username,password,execmd[port1;port2;p]]
        :param loc:
        :return:
        """
        print value
        hostname, port, username, password, count_num, descr  = value.split(',')

        try:
                paramiko.util.log_to_file("paramiko.log")
                s = paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(hostname=hostname, port=int(port), username=username, password=password)
                tt = s.invoke_shell()
                tt.send('configure terminal')
                tt.send('\n')
                tt.send('dpi')
                tt.send('\n')
                tt.send('show dpi blacklist')
                tt.send('\n')
                tt.send(' ')
                while not tt.recv_ready():
                        print "working..."
                        time.sleep(15)
                info = tt.recv(4096)
                s.close()
                if info.count('Rule Index') == int(count_num):
                        if descr in info:
                                print u"黑名单下发成功."
                        else:
                                return u"下发黑名单不匹配."
                else:
                        return u"黑名单开启数量不匹配."

        except:
                return u"DPI 连接失败"
##############################################################################################
#                                                                                                                                                                                         #
#                                                                 MiddleWare  关键字  START                                                                         #
#                                                                                                                                                                                         #
##############################################################################################

@Action.add_action('login')
def action_login(action_object, step_desc, value, loc):
        """
        构造登录使用的公用方法
        """
        print loc, value
        username, password, VerifyNo = value.split(',')
        action_object.find_element(('id', 'login_text_username')).clear()
        action_object.find_element(('id', 'login_text_username')).send_keys(username)
        action_object.find_element(('id', 'login_text_password')).clear()
        action_object.find_element(('id', 'login_text_password')).send_keys(password)
        action_object.find_element(('id', 'login_text_verifycode')).clear()
        action_object.find_element(('id', 'login_text_verifycode')).send_keys(VerifyNo)
        action_object.find_element(('id', 'login_button_loginButton')).click()
        time.sleep(0.5)


@Action.add_action('logout')
def action_logout(action_object, step_desc, value, loc):
        """
        注销通用方法
        """
        action_object.find_element(('id', 'header_a_navUser')).click()
        action_object.find_element(('css', '#header_li_logOut > a')).click()

@Action.add_action('addtopo')
def action_addtopo(action_object, step_desc, value, loc):
        """
        click all elements
        """
        try:
                btn = action_object.find_elements(loc)
                # if btn:
                #         for i in btn:
                #                 i.click()
                #                 time.sleep(2.5)
                #
                list = len(btn)
                print list
                for i in xrange(list):
                        action_object.find_element(('id', 'securitydevice-securityNewDeviceTable_a_addModal_0')).click()
                        time.sleep(2.5)
        except:
                print 'Not found new device.'

@Action.add_action('clearTopo')
def action_clear_topo(action_object, step_desc, value, loc):
        """
        clear 拓扑
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return:
        """
        if action_object.isElementExsit(('id','topology-singleTopo_button_downloadTopo')):
                try:
                        action_object.find_element(('css','button[class="btn btn-default dropdown-toggle ng-scope"]')).click()
                        action_object.find_element(('css','ul[class="dropdown-menu pull-right ng-scope"]')).click()
                        time.sleep(2)
                        action_object.find_element(('css','button[ng-click="confirm()"]')).click()
                except Exception,e:
                        print "clear topo failed!"
        time.sleep(3)

@Action.add_action('Reset')
def action_reset(action_object, step_desc, value, loc):
        """
        重置或重启系统
        :param action_object:
        :param step_desc:
        :param value: restart | reset
        :param loc:
        :return:
        """
        time.sleep(1)
        # 点击系统重置
        action_object.find_element(('css', '#setting-systemconsole_li_systemReset a')).click()
        time.sleep(1)
        if value.upper() == 'RESTART':
                # 点击重启设备
                action_object.find_element(('css', '#setting-systemconsole_button_restartModal')).click()
                time.sleep(1)
                # 点击确定
                action_object.find_element(('css', '.modal-content button:nth-child(2)')).click()
        else:
                # 点击重置系统
                action_object.find_element(('css', '#setting-systemconsole_button_resetModal')).click()
                time.sleep(1)
                # 点击确定
                action_object.find_element(('css', '.modal-content button:nth-child(2)')).click()

        time.sleep(20)
        for i in xrange(30):
                print i+1
                action_object.driver.refresh()
                try:
                        if action_object.find_element(('css', '#login_text_username')) is not None:
                                break
                except:
                        pass
                time.sleep(10)

@Action.add_action('restartmw')
def action_restartmw(action_object, step_desc, value, loc):
        """
        重启MW设备
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return:
        """
        url = action_object.driver.current_url
        hostname = re.search('\d+\.\d+\.\d+\.\d+',url).group(0)
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
                return u"MW 连接失败"
        time.sleep(20)
        for i in xrange(30):
                print i+1
                action_object.driver.get("https://"+hostname+"/login")
                try:
                        if action_object.find_element(('css', '#login_text_username')) is not None:
                                break
                except:
                        pass
                time.sleep(10)

@Action.add_action('Setadmin')
def action_setadmin(action_object, step_desc, value, loc):
        """
        设置admin初始密码
        :param action_object:
        :param step_desc:
        :param value:password
        :param loc:
        :return:
        """
        time.sleep(1)
        # 选择分区管理
        action_object.find_element(('css', '#header_li_domain a')).click()
        time.sleep(1)
        # 输入密码
        action_object.find_element(('css', '#domain_password_newPassword')).send_keys(value)
        time.sleep(0.5)
        # 输入确认密码
        action_object.find_element(('css', '#domain_password_confPassword')).send_keys(value)
        time.sleep(2)
        action_object.find_element(('id', 'domain_button_saveUser')).click()
        time.sleep(0.5)
        if action_object.find_element(('css', '.close')) is not None:
                action_object.find_element(('css', '.close')).click()
        time.sleep(5)

@Action.add_action('redirect')
def sshclient_execmd_redirection(action_object, step_desc, value, loc):
        """
        重新指派DPI
        :param action_object:
        :param step_desc:
        :param value:[hostname,port,username,password,[mw_ip;start|stop]]
        :param loc:
        :return:
        """
        print value
        hostname,port,username,password,execmd=value.split(',')
        try:
                dpi_ip,status = execmd.split(';')
        except:
                dpi_ip = execmd
                status = 'start'
        try:
                paramiko.util.log_to_file("paramiko.log")
                s = paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(hostname=hostname, port=int(port), username=username, password=password)

                if status == 'stop':
                        tt = s.invoke_shell()
                        tt.send('configure terminal')
                        tt.send('\n')
                        tt.send('manager-ui ip '+dpi_ip)
                        tt.send('\n')
                        tt.send('write file')
                        tt.send('\n')
                        tt.send('stop dpi')
                        tt.send('\n')
                        time.sleep(15)
                        while not tt.recv_ready():
                                print "working..."
                                time.sleep(20)
                        print tt.recv(4096)
                        s.close()
                else:
                        tt = s.invoke_shell()
                        tt.send('configure terminal')
                        tt.send('\n')
                        tt.send('manager-ui ip '+dpi_ip)
                        tt.send('\n')
                        tt.send('write file')
                        tt.send('\n')
                        tt.send('stop dpi')
                        tt.send('\n')
                        time.sleep(15)
                        while not tt.recv_ready():
                                print "working..."
                                time.sleep(20)
                        print tt.recv(4096)
                        s.close()
                        st = paramiko.SSHClient()
                        st.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        st.connect(hostname=hostname, port=int(port), username=username, password=password)
                        ts = st.invoke_shell()
                        ts.send('configure terminal')
                        ts.send('\n')
                        ts.send('start dpi')
                        ts.send('\n')
                        while not ts.recv_ready():
                                print "working..."
                                time.sleep(10)
                        print ts.recv(4096)
                        st.close()
        except:
                return u"DPI 连接失败"

@Action.add_action('dpinetport')
def sshclient_dpinetport(action_object, step_desc, value, loc):
        """
        验证DPI端口映射下发
        :param action_object:
        :param step_desc:
        :param value:[hostname,port,username,password,execmd[port1;port2;p]]
        :param loc:
        :return:
        """
        print value
        hostname,port,username,password,execmd=value.split(',')
        try:
                l2 = execmd.split(';')
        except:
                return u'没有填写验证端口'
        try:
                paramiko.util.log_to_file("paramiko.log")
                s = paramiko.SSHClient()
                s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                s.connect(hostname=hostname, port=int(port), username=username, password=password)
                tt = s.invoke_shell()
                tt.send('configure terminal')
                tt.send('\n')
                tt.send('dpi')
                tt.send('\n')
                tt.send('show dpi netport')
                tt.send('\n')
                tt.send(' ')
                while not tt.recv_ready():
                        print "working..."
                        time.sleep(15)
                info = tt.recv(4096)
                s.close()
                a = info.split('\r\n')
                portlist = []
                for i in a:
                        portlist.append(i[i.find(': ')+2:i.find(' (')])
                portlist = list(set(portlist))
                portlist.remove('')
                l1 = set(portlist)
                l2 = set(l2)
                if len(l1 -l2) == 0:
                        print u"端口映射下发DPI成功"
                else:
                        print l1
                        return u"端口映射下发DPI失败"
        except:
                return u"DPI 连接失败"

@Action.add_action('sendTrafoFlowData')
def action_sendTrafoFlowData(action_object, step_desc, value, loc):
        """
        通过trafo发送指定类型的 pcap 包
        :param action_object:
        :param step_desc:
        :param value:类型
        :param loc:
        :return:
        """
        trafoServerIp, datatype = value.split(',')
        SimulatorUtil.sendTrafoFlowData(simulatorIP='192.168.110.77:4000', trafoServerIp=trafoServerIp, type=datatype, timeoutSeconds=None)

@Action.add_action('sendEventAndIncident')
def action_sendEventAndIncident(action_object, step_desc, value, loc):
        """
        发送指定类型的 Event
        :param action_object:
        :param step_desc:
        :param value:类型
        :param loc:
        :return:
        """

        try:
                testServerIP, dpisn = value.split(',')
                print testServerIP,dpisn
        except Exception:
                return "type error!!!"
        SimulatorUtil.sendEventAndIncident(simulatorIP='192.168.110.77:4000', testServerIP=testServerIP, dpisn=dpisn, type='incident')

@Action.add_action('countnum')
def action_countnum(action_object, step_desc, value, loc):
        """
        统计元素出现个数是否与预期一致
        :param action_object:
        :param step_desc:
        :param value: 预期结果
        :param loc:
        :return:
        """
        countnum = action_object.find_elements(loc)
        countnum = len(countnum)
        value = int(value)
        print u"预期结果："+str(value)
        if countnum == value:
                print u"实际结果："+str(countnum)
        else:
                return u"实际结果："+str(countnum)

@Action.add_action('Ele2countnum')
def action_ele_2_countnum(action_object, step_desc, value, loc):
        """
        通过正则匹配获取数字与元素统计进行比较
        :param action_object:
        :param step_desc:
        :param value: 通过正则匹配获取数字[元素]
        :param loc: 元素列表
        :return:
        """
        countnum = action_object.find_elements(loc)
        countnum = len(countnum)

        showtext = action_object.find_element(("xpath", value)).text
        str1 = re.compile(r'\d+')
        shownum = str1.findall(showtext)[0]

        print u"元素统计数量：" + str(countnum)
        if countnum == int(shownum):
                print u"界面显示：" + str(shownum)
        else:
                return u"界面显示：" + str(shownum)

@Action.add_action('ntpsyn')
def action_ele_2_countnum(action_object, step_desc, value, loc):
        """
        通过正则匹配获取数字与元素统计进行比较
        :param action_object:
        :param step_desc:
        :param value: 通过正则匹配获取数字[元素]
        :param loc: 元素列表
        :return:
        """
        system_time = action_object.find_element(('css','#setting_systemconsole_container_editNtpSync input.time-picker-input')).get_attribute('placeholder')
        local_time = (action_object.find_element(('css','#setting_systemconsole_container_editNtpSync div.local-time')).text)
        if system_time[:5] != local_time.split(' ')[1][:5]:
                return u'系统时间与本地时间不一至'

@Action.add_action('untilshow')
def action_untilshow(action_object, step_desc, value, loc):
        """
        持续监听页面元素状态（智能等待），直到发现元素
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return:
        """
        for i in xrange(300):
                try:
                        if action_object.find_element(loc) is not None:
                                break
                except:
                        pass
                time.sleep(1)

@Action.add_action('ipmac_switch')
def action_ipmac_switch(action_object, step_desc, value, loc):
        """
        IP/MAC绑定按钮
        :param action_object:
        :param step_desc:
        :param value: 开启/关闭
        :param loc:
        :return:
        """
        loc_status = action_object.find_element(('xpath', '//span[text()="IP/MAC地址绑定"]/following-sibling::span//label')).text
        if value == u"开启":
                if loc_status == u"关闭":
                        action_object.find_element(('id', 'rule-ipmac_checkbox')).click()
        else:
                if loc_status == u"开启":
                        action_object.find_element(('id', 'rule-ipmac_checkbox')).click()

@Action.add_action('security_detail')
def action_security_detail(action_object, step_desc, value, loc):
    """
        功能模式切换
        :param action_object:
        :param step_desc:
        :param value: 路由保护模式/智能保护模式
        :param loc:
        :return:
        """
    securitydetail = action_object.find_element(('xpath', '//h5[text()="功能模式"]/following-sibling::p')).text
    # loc_status = action_object.find_element(('xpath', '//span[text()="IP/MAC地址绑定"]/following-sibling::span//label')).text
    if value == u"路由保护模式":
        if securitydetail == u"智能保护模式":
            action_object.find_element(('css', 'button[ng-hide="securitydetail.isEdited"]')).click()
            Select(action_object.find_element(('css','div[ng-show="securitydetail.isEdited"]>select'))).select_by_visible_text(u"路由保护模式")
            action_object.find_element(('css', 'button[ng-click="securitydetail.editDone(\'basic\')"]')).click()
            time.sleep(60)
    else:
        if securitydetail == u"路由保护模式":
            action_object.find_element(('css', 'button[ng-hide="securitydetail.isEdited"]')).click()
            Select(action_object.find_element(('css', 'div[ng-show="securitydetail.isEdited"]>select'))).select_by_visible_text(u"智能保护模式")
            time.sleep(1)
            action_object.find_element(('id', 'confirmPanel_button_confirm')).click()
            time.sleep(1)
            action_object.find_element(('css', 'button[ng-click="securitydetail.editDone(\'basic\')"]')).click()
            time.sleep(60)

@Action.add_action('click_add_rule')
def action_security_detail(action_object, step_desc, value, loc):
        """
        click add rule button
        :param action_object:
        :param step_desc:
        :param value:
        :param loc:
        :return:
        """
        if action_object.isElementExsit(('id','rule-blackList-policyDetail_button_createRules')):
                try:
                        action_object.find_element(('id','rule-blackList-policyDetail_button_createRules')).click()
                        time.sleep(2)
                except Exception,e:
                        print "not found add rule button"
#                                                                                                                                                                                         #
#                                                                 MiddleWare  关键字  END                                                                                 #
##############################################################################################









##############################################################################################
#                                                                                                                                                                                         #
#                                                                 漏洞挖掘  关键字  START                                                                                 #
#                                                                                                                                                                                         #
##############################################################################################

@Action.add_action('delete_task')
def delete_task(action_object, step_desc, value, loc):
        """
        删除漏挖任务
        """
        action_object.find_element(("xpath", "//input[@placeholder='输入关键字']")).clear()
        action_object.find_element(("xpath", "//input[@placeholder='输入关键字']")).send_keys(value)
        time.sleep(2)
        action_object.find_element(("xpath", "//button[@tooltip='删除']")).click()
        time.sleep(2)
        action_object.find_element(("xpath", "//button[@ng-click='deleteTask()']")).click()
        action_object.find_element(("xpath", "//input[@placeholder='输入关键字']")).clear()

@Action.add_action('create_louwa_task')
def create_louwa_task(action_object, step_desc, value, loc):
        """
        新建漏挖任务
        """
        para = re.split(',', value)
        action_object.find_element(("id", "task-work-panel")).click()
        time.sleep(1)
        action_object.find_element(("id", "create-louwa-task")).click()
        time.sleep(1)
        action_object.find_element(("id", "louwa-task-name")).send_keys(para[0])
        action_object.find_element(("id", "louwa-project-choose")).click()
        time.sleep(1)
        action_object.find_element(("xpath", "//*[@id='louwa-project-choose']/li[@title='%s']" % para[1])).click()
        time.sleep(1)
        action_object.find_element(("id", "task-type-choose")).click()
        time.sleep(1)
        action_object.find_element(("xpath", "//*[@id='task-type-choose']/li")).click()
        time.sleep(1)
        action_object.find_element(("id", "bus-type-choose")).click()
        time.sleep(1)
        action_object.find_element(("xpath", "//*[@id='bus-type-choose']/li[contains(text(),'%s')]" % para[2])).click()
        time.sleep(1)
        if int(para[3]) == 0:
                action_object.find_element(("xpath", "//*[@id='is-create-louwa-task']/button[1]")).click()
        elif int(para[3]) == 1:
                action_object.find_element(("xpath", "//*[@id='is-create-louwa-task']/button[2]")).click()
        elif int(para[3]) == 2:
                action_object.find_element(("xpath", "//*[@id='is-create-louwa-task']/button[3]")).click()

@Action.add_action('check_description')
def check_description(action_object, step_desc, value, loc):
        """
        检查描述框的值是否符合预期
        """
        description = action_object.find_element(("xpath", "//textarea[@ng-model='unsavedTask.desc']")).get_attribute("value")
        if value == description:
                print u'描述信息正确'
        else:
                return u'描述信息错误'


#                                                                                                                                                                                          #
#                                                                漏洞挖掘  关键字  END                                                                                         #
##############################################################################################



##############################################################################################
#                                                                                                                                                                                         #
#                                                                 威胁评估  关键字  START                                                                                 #
#                                                                                                                                                                                         #
##############################################################################################
@Action.add_action('loginGemstoneInput')
def action_loginGemstoneInput(action_object, step_desc, value, loc):
        """
        构造Gemstone登录时输入用户名和密码的公用方法
        """
        print value
        username, password = value.split(',')
        action_object.find_element(('xpath', "//input[@placeholder='请输入用户名']")).clear()
        action_object.find_element(('xpath', "//input[@placeholder='请输入用户名']")).send_keys(username)
        action_object.find_element(('xpath', "//*[@placeholder='请输入密码']")).clear()
        action_object.find_element(('xpath', "//*[@placeholder='请输入密码']")).send_keys(password)
        time.sleep(0.5)

@Action.add_action('createGemProject')
def action_createGemProject(action_object, step_desc, value,loc):
        """
        构造Gemstone创建项目的公用方法[projectName, province, city, area[2,]]
        """
        print value
        try:
                projectName, province, city, area = value.split(',')
        except:
                projectName, province, city = value.split(',')
        try:
                action_object.find_element(('xpath', "//div[@class='mask-help']//a[@ng-click='closeMaskLayer()']")).click()
        except:
                print u'已经有项目存在了'
        action_object.find_element(('xpath', "//div[@class='project-item-image']//i")).click()
        action_object.find_element(('xpath', "//input[@name='projectName']")).clear()
        action_object.find_element(('xpath', "//input[@name='projectName']")).send_keys(projectName)
        action_object.find_element(('xpath', "//*[@id='areaChoosed']")).click()
        action_object.find_element(('xpath', "//a[text()='%s']" % province)).click()
        action_object.find_element(('xpath', "//a[text()='%s']" % city)).click()
        time.sleep(1)
        try:
                area_list = area.split(';')
                if len(area_list) >0:
                        action_object.find_element(('xpath', "//ul[@class='category-list']//li[2]")).click()
                        for i in range(len(area_list)):
                                action_object.find_element(('xpath', "//button[@ng-click='infoCtrl.addZone()']")).click()
                                time.sleep(0.5)
                                elements = action_object.find_elements(('xpath', "//input[contains(@ng-model,'zone')]"))
                                elements[i+1].click()
                                elements[i+1].send_keys(area_list[i])
                        time.sleep(0.5)
        except:
                print u'只需要1个默认区域.'


@Action.add_action('autoScan_ManaualInput')
def autoScan_ManaualInput(action_object, step_desc, value, loc):
        """
        构造Gemstone的公用方法，选择分析区域和填写方式，不点击保存[区域, 手动录入]
        """
        area, method = value.split(',')
        action_object.find_element(('xpath', "//div[@class='project-item-image']")).click()
        action_object.find_element(('xpath', "//form[@name='assetAnalysisForm']//div[contains(.,'资产分析区域')]//button")).click()
        action_object.find_element(('xpath', "//a[contains(@ng-click,'entryCtrl') and text()='%s']" %area)).click()
        action_object.find_element(('xpath', "//form[@name='assetAnalysisForm']//div[contains(.,'填写方式')]//button")).click()
        action_object.find_element(('xpath', "//a[contains(text(),'%s')]" %method)).click()


@Action.add_action('enter_device_info')
def enter_device_info(action_object, step_desc, value, loc):
        """
        构造Gemstone添加设备的公用方法，没有点击保存的步骤.
        enter_device_info(type, vendor, xinghao, 1.1.1.1)
        """
        print value
        value_list= value.split(',')
        type, vendor, xinghao = value.split(',')[:3]
        time.sleep(1)
        action_object.find_element(('xpath', "//div[@options='manualCtrl.deviceTypes']//button")).click()
        time.sleep(1)
        action_object.find_element(('xpath', "//a[contains(.,'%s')]" %type)).click()
        action_object.find_element(('xpath', "//div[@options='manualCtrl.deviceVendors']//button")).click()
        time.sleep(1)
        action_object.find_element(('xpath', "//a[contains(.,'%s')]" %vendor)).click()
        action_object.find_element(('xpath', "//div[@options='manualCtrl.deviceNames']//button")).click()
        time.sleep(1)
        action_object.find_element(('xpath', "//a[contains(.,'%s')]" %xinghao)).click()
        if len(value_list)==4:
                ip_1 = value_list[3]
                action_object.find_element(('xpath', "//input[@name='ipAddress']")).send_keys(ip_1)

@Action.add_action('setLinkArea')
def setLinkArea(action_object, step_desc, value, loc):
        """
        构造Gemstone添加设备的公用方法，没有点击保存的步骤.
        setLinkArea(区域)
        """
        print value
        linkButton = action_object.find_element(('xpath', "//button[@class='add-zone-btn']"))
        ActionChains(action_object.driver).move_to_element(linkButton).perform()
        linkButton.click()
        action_object.find_element(('xpath', "//div[@class='dropdown']/span")).click()
        action_object.find_element(('xpath', "//a[text()='%s']" %value)).click()



@Action.add_action('select_delete_device')
def select_delete_device(action_object, step_desc, value, loc):
        """
        删除设备信息：all-删除所有的；xpath：删除满足条件的
        """
        if value == 'all':
                elements = action_object.find_elements(('xpath',"//div[@class='pcap-item-left']"))
        else:
                elements = action_object.find_elements(('xpath',"//h6[text()='%s']" %value))
        action_object.find_element(('xpath',"//span[text()='批量操作']")).click()
        for ele in elements:
                ele.click()
        action_object.find_element(('xpath',"//div[@ng-click='listCtrl.delete()']")).click()




@Action.add_action('assertTrueByXpath')
def assertTrueByXpath(action_object, step_desc, value, loc):
        print u'预期结果：元素存在'
        '''try:
                action_object.find_element(('xpath',value))
                return True
        except:
                return False'''
        if action_object.isElementExsit(('xpath',value)):
                print u'实际结果：元素存在'
        else:
                action_object.saveScreenshot("assertTrueError")
                return u'实际结果：元素不存在'

@Action.add_action('assertFalseByXpath')
def assertFalseByXpath(action_object, step_desc, value, loc):
        print u'预期结果：元素不存在'
        if action_object.isElementExsit(('xpath',value)):
                action_object.saveScreenshot("assertFalseError")
                return u'实际结果：元素存在'
        else:
                print u'实际结果：元素不存在'

@Action.add_action('enterAutoScanInfo')
def enterAutoScanInfo(action_object, step_desc, value, loc):
        """
        输入自动扫描的信息[eth1,192.168.1.23/23,192.168.1.23]
        """
        eth, scanRange, scanPort = value.split(',')
        print u'选择网口'
        action_object.find_element(('xpath', "//form[@name='assetAnalysisForm']//div[contains(.,'连接网口')]//button")).click()
        action_object.find_element(('xpath', "//a[contains(.,'%s')]" %eth)).click()
        print u'输入扫描范围'
        action_object.find_element(('xpath', "//textarea[@name='ipAddress']")).clear()
        action_object.find_element(('xpath', "//textarea[@name='ipAddress']")).send_keys(scanRange)
        print u'输入扫描口IP'
        action_object.find_element(('xpath', "//input[@name='scanPortIp']")).clear()
        action_object.find_element(('xpath', "//input[@name='scanPortIp']")).send_keys(scanPort)
        action_object.find_element(('xpath', "//input[@name='scanSubnet']")).click()

@Action.add_action('controlAutoScan')
def controlAutoScan(action_object, step_desc, value, loc):
        """
        value： 1-等待扫描完成； 2-停止不保存， 3-停止， 4-取消停止
        """
        result = False
        flag = value
        if flag=='1':
                for i in range(600):
                        try:
                                action_object.find_element(('xpath', "//div[@class='scan-header']//span[@ng-if='topologyCtrl.showResult']"))
                                result = True
                        except:
                                time.sleep(1)
        elif flag=='2':
                action_object.find_element(('xpath', "//button[text()='停止']")).click()
                time.sleep(1)
                action_object.find_element(('xpath', "//button[text()='停止' and @ng-click='confirmCtrl.ok()']")).click()
        elif flag=='3':
                action_object.find_element(('xpath', "//button[text()='停止']")).click()
                time.sleep(1)
                action_object.find_element(('xpath', "//button[text()='停止并保存']")).click()
        elif flag=='4':
                action_object.find_element(('xpath', "//button[text()='停止']")).click()
                time.sleep(1)
                action_object.find_element(('xpath', "//button[text()='取消']")).click()

@Action.add_action('deleteAssetAreaData')
def deleteAssetAreaData(action_object, step_desc, value, loc):
        """
        删除区域资产信息  [区域1,区域2,确定]
        """
        print value
        value_list= value.split(',')
        area_num = action_object.find_element(('xpath', "//span[@class='account ng-binding']")).text
        area_num = area_num.split(u'（')[1].split(u'）')[0]
        if area_num !='0':
                time.sleep(1)
                action_object.find_element(('xpath', "//span[text()='批量操作']")).click()
                for area in value_list[:-1]:
                        action_object.find_element(('xpath', "//p[text()='%s']/.." %area)).click()
                action_object.find_element(('xpath', "//div[@ng-click='assetCtrl.delete()']")).click()
                time.sleep(1)
                confirm_or_cancel = value_list[-1]
                action_object.find_element(('xpath', "//button[contains(text(),'%s')]" %confirm_or_cancel)).click()
                time.sleep(2)

@Action.add_action('openQuestionnaire')
def openQuestionnaire(action_object, step_desc, value, loc):
        """
        打开威胁分析问卷[问卷名]
        """
        print value
        form_name,action= value.split(',')
        if action == u'开始':
                action_object.find_element(('xpath',"//div[contains(text(), '%s')]/../../div[1]" % form_name)).click()
        elif action == u'继续编辑':
                action_object.find_element(('xpath',"//div[contains(text(), '%s')]/../../div[1]" % form_name)).click()
        elif action == u'清空重填':
                action_object.find_element(('xpath',"//div[contains(text(), '%s')]/..//button" % form_name)).click()
                action_object.find_element(('xpath',"//button[@ng-click='confirmCtrl.ok()']")).click()
        time.sleep(1)
#//li[@class='nav-item ng-scope selected complete']
@Action.add_action('fillQuestionnaire')
def fillQuestionnaire(action_object, step_desc, value, loc):
        """
        填写威胁分析问卷[0-是|1-否|2-其他]
        """
        print value
        answer= int(value)
        time.sleep(1)
        #为工控系统安全检查指标时
        if action_object.isElementExsit(('xpath',"//div[contains(text(),'工控系统安全检查指标')]")):
                question_block_list = action_object.find_elements(('xpath', "//div[@class='panel-group']//li"))
        else:
                question_block_list = action_object.find_elements(('xpath', "//ul//div[contains(@class,'mCSB_container')]//li"))
        question_catagory_xpath = "//ul[@ng-repeat='score in threatEditCtrl.scoreData track by $index']"
        for question_block in question_block_list:
        #uncomment here
                ActionChains(action_object.driver).move_to_element(question_block).perform()
                question_block.click()
                time.sleep(1)
                question_catagorys = action_object.find_elements(('xpath',question_catagory_xpath))
                for question_catagory in question_catagorys:
                        question_title_clickables = question_catagory.find_element_by_xpath(".//li[1]") #找出所有的title 1. XXX; 2.XXX.....
                        # print 'find all div'value
                        question_title_clickables = question_title_clickables.find_elements_by_xpath(".//span[@class='checkItem ng-scope']//div")
                        if len(question_title_clickables) == 0:
                                question_bodys = question_catagory.find_elements_by_xpath(".//li[contains(@class,'pointer ng-scope')]")
                                #action_object.driver.wait_until_visible(".//span[@class='checkItem']//div[contains(@class,'radioBox')]")
                                question_body_clickables = question_bodys[0].find_elements_by_xpath(".//span[@class='checkItem']//div[contains(@class,'radioBox')]")
                                ActionChains(action_object.driver).move_to_element(question_body_clickables[answer]).perform()
                                try:
                                        question_body_clickables[answer].click()  #answer： 0-yes， 1-no， 2-others
                                except:
                                        ActionChains(action_object.driver).move_to_element(question_bodys[0].find_element_by_xpath(".//span[@class='checkItem']//div[not(contains(@class,'ng-hide'))]//input")).perform()
                                        question_bodys[0].find_element_by_xpath(".//span[@class='checkItem']//div[not(contains(@class,'ng-hide'))]//input").send_keys('1')
                        else:
                                question_title_clickable = question_title_clickables[answer]
                                ActionChains(action_object.driver).move_to_element(question_title_clickable).perform()
                                question_title_clickable.click()
        action_object.driver.refresh()
        time.sleep(2)

@Action.add_action('fillCurrentPage')
def fillCurrentPage(action_object, step_desc, value, loc):
        """
        填写当前页面的question为是|否 [yes|no]
        """
        print value
        subs = action_object.find_elements(('xpath',"//div[contains(@ng-click,'%s')]//label" % value))
        for sub in subs:
                ActionChains(action_object.driver).move_to_element(sub).perform()
                sub.click()
                time.sleep(0.2)


#######################################流量分析相关关键字#########################################
@Action.add_action('setTrafficArea')
def setTrafficArea(action_object, step_desc, value, loc):
        """
        设置流量截取的区域[区域]
        """
        print value
        action_object.find_element(('xpath',"//div[@class='project-item-image']")).click()
        action_object.find_element(('xpath',"//button[@class='standard ges-btn-dropdown dropdown-toggle ng-binding']")).click()
        action_object.find_element(('xpath',"//ul//a[text()='%s']" % value)).click()
        action_object.find_element(('xpath',"//button[contains(@ng-click,'entryCtrl.ok')]")).click()

@Action.add_action('setTrafficParameter')
def setTrafficParameter(action_object, step_desc, value, loc):
        """
        设置流量截取的区域[区域]
        """
        print value
        size, hour, min, second, port = value.split(',')
        action_object.find_element(('xpath', "//div[@class='add-icon' and @ng-click='trafficPcCtrl.startEntry()']")).click()
        action_object.find_element(('xpath', "//input[@name='pcapSize']")).clear()
        action_object.find_element(('xpath', "//input[@name='pcapSize']")).send_keys(size)
        action_object.find_element(('xpath', "//input[@name=' hour']")).clear()
        action_object.find_element(('xpath', "//input[@name=' hour']")).send_keys(hour)
        action_object.find_element(('xpath', "//input[@name=' minutes']")).clear()
        action_object.find_element(('xpath', "//input[@name=' minutes']")).send_keys(min)
        action_object.find_element(('xpath', "//input[@name=' seconds']")).clear()
        action_object.find_element(('xpath', "//input[@name=' seconds']")).send_keys(second)
        action_object.find_element(('xpath', "//div[@class='value-info dropdown']")).click()
        action_object.find_element(('xpath', "//a[text()='%s']" % port)).click()

@Action.add_action('rightCornerNav')
def rightCornerNav(action_object, step_desc, value, loc):
        """
        打开右上角对应的导航[账户,账户管理]
        """
        print value
        value_list = value.split(',')
        if value_list[0]== u'帮助':
                action_object.find_element(('xpath', "//div[@ng-click='projectCtrl.gotoHelp()']")).click()
        elif value_list[0]== u'账户':
                action_object.find_element(('xpath', "//div[contains(@ng-class,'is_show_user_menu')]")).click()
                action_object.find_element(('xpath', "//a[contains(text(),'%s')]" %value_list[1])).click()
        elif value_list[0]== u'设置':
                action_object.find_element(('xpath', "//div[contains(@ng-class,'is_show_system_menu')]")).click()
                action_object.find_element(('xpath', "//a[contains(text(),'%s')]" %value_list[1])).click()
        elif value_list[0]== u'系统':
                action_object.find_element(('xpath', "//div[contains(@ng-class,'is_show_power_menu')]")).click()
                action_object.find_element(('xpath', "//a[contains(text(),'%s')]" %value_list[1])).click()

@Action.add_action('enterNewUserInfo')
def enterNewUserInfo(action_object, step_desc, value, loc):
        """
        输入用户名和密码[username,passwd,repeatPasswd]
        """
        print value
        userName, passwd,rePasswd = value.split(',')
        action_object.find_element(('xpath', "//input[@name='loginName']")).clear()
        action_object.find_element(('xpath', "//input[@name='loginName']")).send_keys(userName)
        action_object.find_element(('xpath', "//input[@name='newPassword']")).clear()
        action_object.find_element(('xpath', "//input[@name='newPassword']")).send_keys(passwd)
        action_object.find_element(('xpath', "//input[@name='repeatPassword']")).clear()
        action_object.find_element(('xpath', "//input[@name='repeatPassword']")).send_keys(rePasswd)

@Action.add_action('searchUser')
def searchUser(action_object, step_desc, value, loc):
        """
        搜索[username]
        """
        print value
        action_object.find_element(('xpath', "//input[@ng-model='usersCtrl.searchKeyWord']")).clear()
        action_object.find_element(('xpath', "//input[@ng-model='usersCtrl.searchKeyWord']")).send_keys(value)
        time.sleep(1)


@Action.add_action('deleteUser')
def deleteUser(action_object, step_desc, value, loc):
        """
        删除用户[username,删除用户|取消]
        """
        print value
        userName, comfirm = value.split(',')
        de = u'删除'
        xpath="//div[@class='login-name']//span[text()='" +userName +"']/../..//i[@uib-tooltip='"+ de +"']"
        action_object.find_element(('xpath', xpath)).click()
        action_object.find_element(('xpath', "//button[text()='%s']" %comfirm)).click()




@Action.add_action('checkHelp')
def checkHelp(action_object, step_desc, value, loc):
        """
        检查帮助各个标题的内容及Link
        """
        stored_titles = [[u'如何进行项目管理', u'创建新项目', u'批量操作',u'项目排序', u'项目搜索'],
                           [u'如何进行威胁分析', u'威胁分析管理页面', u'开始威胁分析', u'查看威胁分析结果'],
                           [u'如何进行资产分析', u'手动添加设备',u'自动识别设备',u'编辑设备',u'批量操作',u'计算区域威胁评分', u'资产拓扑', u'查看评分总览'],
                           [u'如何进行流量分析', u'流量分析管理页面', u'流量分析设置', u'开始流量分析', u'导入流量分析', u'实时分析结果', u'流量统计页面'],
                           [u'如何进行无线分析', u'无线分析管理页面', u'开始无线分析', u'无线分析结果'],
                           [u'如何进行拓扑分析'],
                           [u'如何进行报告管理'],
                           [u'如何进行系统管理',u'恢复出厂设置', u'日志管理', u'系统设置', u'系统升级', u'系统导出', u'版本信息', u'账户管理', u'退出', u'关机', u'重新启动']]
        result = True
        time.sleep(1)
        the_first_level_nav = action_object.find_elements(('xpath',"//div[contains(@class, 'panel panel-default')]"))
        for i in range(0,len(the_first_level_nav)):
                the_first_level_xpah = "//div[contains(@class, 'panel panel-default')][%s]"%(i+1)
                if i != 0:
                        action_object.find_element(('xpath',the_first_level_xpah)).click()
                        time.sleep(0.2)
                the_selected_first_level_xpath = "//div[contains(@class,'panel-default')][%s]//div[contains(@class,'selected')]"%(i+1)
                the_opened_second_level_nav = action_object.find_elements(('xpath',"//div[@class='panel-collapse in collapse']//span"))
                first_level_title_left_nav = action_object.find_element(('xpath',the_selected_first_level_xpath)).text
                first_level_title_right = action_object.find_element(('xpath',"//div[@class='help-text ng-scope']/div[contains(@class,'title-name')]")).text
                if first_level_title_left_nav == stored_titles[i][0] and first_level_title_right == stored_titles[i][0]:
                        result = result and True
                else:
                        result = result and False
                if the_opened_second_level_nav != None:
                        if len(the_opened_second_level_nav) > 0:
                                for element in range(0,len(the_opened_second_level_nav)):
                                        if element + 1 == len(the_opened_second_level_nav):
                                                ActionChains(action_object.driver).move_to_element(the_opened_second_level_nav[element]).perform()
                                        the_opened_second_level_nav[element].click()
                                        time.sleep(0.2)
                                        #the_second_title_left_nav = the_opened_second_level_nav[element].text
                                        the_second_title_right = action_object.find_element(('xpath',"//div[@class='help-text ng-scope']//p[contains(@class,'dtitle')]")).text
                                        if the_second_title_right == stored_titles[i][element+1]:
                                                result = result and True
                                        else:
                                                result = result and False
        if result == True:
                print u'帮助各个标题的Link和内容显示正确'
        else:
                return False


@Action.add_action('setWirelessArea')
def setWirelessArea(action_object, step_desc, value, loc):
        """
        设置无线分析的区域[区域]
        """
        print value
        action_object.find_element(('xpath',"//div[@class='project-item-image']")).click()
        action_object.find_element(('xpath',"//button[@class='standard ges-btn-dropdown dropdown-toggle ng-binding']")).click()
        action_object.find_element(('xpath',"//ul//a[text()='%s']" % value)).click()
        action_object.find_element(('xpath',"//button[contains(@ng-click,'startWifiCtrl.ok')]")).click()
#                                                                                                                                                                                          #
#                                                                威胁评估  关键字  END                                                                                         #
##############################################################################################