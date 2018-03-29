# -*- coding: utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2017-01-19
"""
from Base import *


################################################################################
# 关键字函数必须用Aciton.add_action(keyword)装饰起进行装饰
# 函数的形参必须为4个:action_object(Aciton对象), step_desc(步骤描述信息，可用于记录log),
#                  value(需要输入的值，多个输入值用逗号隔开), loc(元素的定位信息)
# 函数正常退出时不能有返回值（使用默认的返回值None），出错时返回字符串（记录出错信息）
################################################################################



##############################################################################################
#                                                                                             #
#                                 自定义关键字  START                                             #
#                                                                                             #
##############################################################################################

@Action.add_action('keau1000_login')
def action_login(action_object, step_desc, value, loc):
    """
    构造登录使用的公用方法
    """
    print value
    username, password = value.split(',')
    action_object.find_element(('id', 'login_txtUserName')).clear()
    action_object.find_element(('id', 'login_txtUserName')).send_keys(username)
    action_object.find_element(('id', 'login_txtUserPassword')).clear()
    action_object.find_element(('id', 'login_txtUserPassword')).send_keys(password)
    # action_object.find_element(('id', 'login_text_verifycode')).clear()
    # action_object.find_element(('id', 'login_text_verifycode')).send_keys(VerifyNo)
    action_object.find_element(('id', 'login_btnLogin')).click()
    time.sleep(0.5)
    try:
        action_object.find_element(('css', 'button.btn-guidestyle.btn-g-over')).click()
    except:
        pass


@Action.add_action('keau1000_reset')
def action_(action_object, step_desc, value, loc):
    """
    reset platform
    """
    # print loc, value
    # username, password = value.split(',')
    url = action_object.driver.current_url
    hostname = re.search('\d+\.\d+\.\d+\.\d+', url).group(0)
    action_object.find_element(('css', 'ul.nav-list li:nth-child(8) span')).click()
    time.sleep(0.5)
    action_object.find_element(('css', 'ul.nav-list li:nth-child(8) div li:nth-child(2)')).click()
    time.sleep(0.5)
    action_object.find_element(('id', 'system_system_btnResetDevice')).click()
    time.sleep(30)
    for i in xrange(180):
        print i + 1,
        action_object.driver.get("https://" + hostname)
        if action_object.isElementExsit(('id', 'login_txtUserName')):
            break
        time.sleep(1)
    action_object.find_element(('id', 'login_txtUserName')).clear()
    action_object.find_element(('id', 'login_txtUserName')).send_keys('admin')
    action_object.find_element(('id', 'login_txtUserPassword')).clear()
    action_object.find_element(('id', 'login_txtUserPassword')).send_keys('admin@123')
    # action_object.find_element(('id', 'login_text_verifycode')).clear()
    # action_object.find_element(('id', 'login_text_verifycode')).send_keys(VerifyNo)
    action_object.find_element(('id', 'login_btnLogin')).click()
    action_object.find_element(('css', 'div.row-setting label[for="device_centralize_rabMode1"]')).click()
    action_object.find_element(('id', 'device_centralize_btnMode')).click()
    time.sleep(30)
    for i in xrange(180):
        print i + 1,
        action_object.driver.get("https://" + hostname)
        if action_object.isElementExsit(('id', 'login_txtUserName')):
            break
        time.sleep(1)
    action_object.find_element(('id', 'login_txtUserName')).clear()
    action_object.find_element(('id', 'login_txtUserName')).send_keys('admin')
    action_object.find_element(('id', 'login_txtUserPassword')).clear()
    action_object.find_element(('id', 'login_txtUserPassword')).send_keys('admin@123')
    # action_object.find_element(('id', 'login_text_verifycode')).clear()
    # action_object.find_element(('id', 'login_text_verifycode')).send_keys(VerifyNo)
    action_object.find_element(('id', 'login_btnLogin')).click()
    time.sleep(1)
    # action_object.find_element(('css', 'button.btn-guidestyle.btn-g-over')).click()
    if action_object.isElementExsit(('id', 'spanSystemTime')):
        print "reset succesful."
    else:
        return "reset failed!"


@Action.add_action('btn_on_off')
def action_btn_on_off(action_object, step_desc, value, loc):
    """
    执行javaScript
    :param action_object:
    :param step_desc:
    :param value: jquery loc , true | flase
    :param loc: javascript
    :return:
    """
    print value
    loc, btn_value = value.split(',')
    js = 'return jQuery("' + loc + '").is(":checked")'
    try:
        rejs = action_object.driver.execute_script(js)
        print rejs
        if str(rejs).lower() == btn_value.lower():
            print u"开关状态验证通过."
        else:
            return u"开关状态验证失败."
    except Exception, e:
        return str(e)

def execute_in_start(hostname,port,username,password,start_pw,cmds):
    from time import sleep
    comands = ['start', start_pw]
    comands.append(isinstance(cmds, (list, tuple)) and ';'.join(cmds) or cmds)
    comands = ['%s\n' % comand for comand in comands]

    try:
        myssh = paramiko.SSHClient()
        myssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        myssh.load_system_host_keys()
        myssh.connect(hostname, int(port), username, password, timeout=300)
    except paramiko.SSHException, err:
        print u'无法连接到 "%s": %s' % (hostname, err)
        return False

    chan = myssh.invoke_shell()
    for comand in comands:
        chan.send(comand)
        sleep(1)
        out = chan.recv(65535)
        while not out.endswith('# ') and not out.endswith(': ') and not out.endswith('$ '):
            sleep(0.5)
            out += chan.recv(65535)

    myssh.close()
    return '\n'.join(out.split(os.linesep)[1:-1])

@Action.add_action('verify_diskrate')
def action_verify_diskrate(action_object, step_desc, value, loc):
    u"""获取设备磁盘信息、计算设备磁盘利用率、获取页面磁盘利用率、比较前后是否一致
    :param value:[hostname,port,username,password,start_pw,id,attr]
    """
    print value
    hostname,port,username,password,start_pw,id,attr=value.split(',')
    print u'开始计算系统的磁盘占用率'
    disk_used = 0
    disk_avail = 0
    df_info = execute_in_start(hostname,port,username,password,start_pw,'df -m')

    # 获取所有分区的使用情况和大小
    disk_info_list = re.findall(re.compile(r"/dev/.+\s+(\d+)\s+(\d+)\s+(\d+)\s+"), df_info)
    for disk_info in disk_info_list:
        disk_used += int(disk_info[1])
        disk_avail += int(disk_info[2])

    # 计算出硬盘使用率
    diskrate_sys = (disk_used * 100) // disk_avail + 1
    print u'系统硬盘占用率为%d' % diskrate_ys

    js = "return $('#%s').attr('%s')" % (id, attr)
    try:
        value = action_object.driver.execute_script(js)
        print u'%s元素的属性值是：%s' % (attr, value)
        if (diskrate_sys - 5 >= int(value)) or (diskrate_sys + 5 <= int(value)):
            return False
    except Exception, err:
        return str(err)

    return None

@Action.add_action('verify_diskrate_increment')
def action_verify_diskrate_increment(action_object, step_desc, value, loc):
    u"""获取页面磁盘利用率、向磁盘写入文件、再次获取页面磁盘利用率、检查增量是否准确、获取设备磁盘信息、计算设备磁盘利用率、比较前后是否一致
    :param value:[hostname,port,username,password,start_pw,id,attr,cmds,increment]
    """
    from time import sleep
    print value
    hostname,port,username,password,start_pw,id,attr,cmds,increment=value.split(',')

    # 页面磁盘利用率
    js = "return $('#%s').attr('%s')" % (id, attr)
    try:
        page_rate_before = int(action_object.driver.execute_script(js))
        print u'页面磁盘利用率: %d' % page_rate_before
    except Exception, err:
        return str(err)

    try:
        # 向磁盘写入文件
        print u'执行 dd 命令向磁盘写入文件'
        execute_in_start(hostname,port,username,password,start_pw,cmds)

        # 写入文件后页面磁盘利用率
        action_object.driver.refresh()
        sleep(2)
        js = "return $('#%s').attr('%s')" % (id, attr)
        try:
            page_rate_after = int(action_object.driver.execute_script(js))
            print u'写入文件后页面磁盘利用率: %d' % page_rate_after
        except Exception, err:
            return str(err)

        # 检查增量是否准确
        if page_rate_before + int(increment) != page_rate_after:
            print u'向磁盘写入文件后磁盘利用率的增量不准确'
            return False

        # 计算系统的磁盘占用率
        disk_used = 0
        disk_avail = 0
        df_info = execute_in_start(hostname,port,username,password,start_pw,'df -m')
        disk_info_list = re.findall(re.compile(r"/dev/.+\s+(\d+)\s+(\d+)\s+(\d+)\s+"), df_info)
        for disk_info in disk_info_list:
            disk_used += int(disk_info[1])
            disk_avail += int(disk_info[2])

        diskrate_sys = (disk_used * 100) // disk_avail + 1
        print u'系统硬盘占用率: %d' % diskrate_sys

        # 比较前后是否一致
        if (diskrate_sys - 5 >= page_rate_after) or (diskrate_sys + 5 <= page_rate_after):
            print u'磁盘利用率前后不一致'
            return False

    finally:
        # 删除文件
        print u'删除写入的磁盘文件'
        execute_in_start(hostname,port,username,password,start_pw,'rm %s' % cmds.split('of=')[1])

    return None

#                                                                                             #
#                                 自定义关键字  END                                             #
##############################################################################################
