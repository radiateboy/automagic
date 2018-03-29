# -*- coding: utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2016-08-03
"""

import argparse
import os
import time
import unittest
import json
import subprocess
import popautomagic
import testrail
import MySQLdb
import HTMLTestRunner
import datetime
from CustomKeyword import *
from Base import Action


class TestSuite(unittest.TestCase):
    def tearDown(self):
        '''
        每个测试用例执行后的收尾函数
        :return:
        '''
        Controller.case_id_list.append(self.case_id)
        Controller.flag_list.append([self.testrail_case_id, self.result_flag])

    def action_test(self, step_list):
        '''
        生成详细的测试用例
        :param step_list:
        :return: None
        '''
        self.case_id, self.testrail_case_id, case_desc = step_list[0][0:3]
        result = None
        print "[%s]" % case_desc
        text = u'[%d:' % self.case_id + case_desc + u']'
        try:
            for idx, step_info in enumerate(step_list):
                stepid = idx
                print u'step%d' % (stepid + 1),
                if stepid >= 0:
                    textstr = text + u'step%d:' % (stepid + 1) + step_info[3:][1]
                    try:
                        Controller.action.show_note(textstr)
                    except:
                        pass
                result = Controller.action_test(*step_info[3:])
                if result is not None:
                    result = u'step%d: %s' % (idx + 1, result)
                    break
        except Exception, e:
            self.result_flag = 2
            text_result = u'【case_%d ERROR】 step%d: %s' % (self.case_id, idx + 1, e)
            print text_result
            Controller.action.save_runing_log(text_result)
            if Controller.video is not None:
                subprocess.Popen("pkill -2 recordmydesktop", shell=True)
            else:
                Controller.action.saveScreenshot(str(self.case_id))
            raise Exception(u'ERROR')
        else:
            if result is None:
                self.result_flag = 1
                text_result =  u'【case_%d PASS】' % self.case_id
                print text_result
                Controller.action.save_runing_log(text_result)
                if Controller.video is not None:
                    subprocess.Popen("pkill -2 recordmydesktop", shell=True)
            else:
                self.result_flag = 5
                text_result =  u'【case_%d FAIL】 %s' % (self.case_id, result)
                print text_result
                Controller.action.save_runing_log(text_result)
                if Controller.video is not None:
                    subprocess.Popen("pkill -2 recordmydesktop", shell=True)
                else:
                    Controller.action.saveScreenshot(str(self.case_id))
                self.assertTrue(False, msg=u'FAIL')

    @staticmethod
    def generateTest(step_list):
        def func(self):
            if Controller.video is not None:
                time.sleep(5)
                image = Controller.action.saveVideoName(step_list[0][0])
                video = subprocess.Popen("recordmydesktop --no-sound -o %s > video.log" % image + ".ogv", shell=True)
                self.action_test(step_list)
                subprocess.Popen("kill -2 %s" % str(video.pid + 1), shell=True)
            else:
                self.action_test(step_list)

        return func


class Controller(object):
    action = None
    client = None
    user = ''
    password = ''
    run_id = None
    result_list = []
    case_id_list = []
    flag_list = []
    expand_paras_dict = None
    conn = None
    cur = None
    args = None
    start = None
    # [all, pass, fail, error, result_path]
    tag_list = [0, 0, 0, 0, '']
    task_type = None
    task_name = None
    video = None

    @classmethod
    def update_task_history(cls):
        if Controller.args.user_id is not None:
            user_id = Controller.args.user_id
            Controller.my_execute(ur'''SELECT id FROM autoplat_user WHERE username = '%s' ''' % Controller.args.user_id)
            task_info = Controller.cur.fetchall()
            if task_info:
                user_id = task_info[0][0]
            exectime = datetime.datetime.now() - Controller.start
            sql_str = ur"""INSERT INTO autoplat_taskhistory (tasktype, taskname, case_tag_all, case_tag_pass,
                        case_tag_fail, case_tag_error, starttime, exectime, taskid_id, userid_id, reporturl, build_name, build_number)
                        VALUES (%s, '%s', %s, %s, %s, %s, '%s', '%s', %s, %s, '%s', '', '')""" % \
                      (Controller.task_type, Controller.task_name, Controller.tag_list[0], Controller.tag_list[1],
                       Controller.tag_list[2], Controller.tag_list[3], Controller.start,exectime,
                       Controller.args.task_id, user_id, Controller.tag_list[4])
            Controller.my_execute(sql_str)
            Controller.conn.commit()
        # 通过钉钉接口，使用钉钉机器人把测试结果发送对应群中
        if Controller.args.popding is not None:
            url = "https://oapi.dingtalk.com/robot/send?access_token=8d36288c964c024ca2e5e53a45faddde0adcb2c6c638e9a59a16096f5d866715"
            #url = "https://oapi.dingtalk.com/robot/send?access_token=e0c23e2f9242783f0ad34ccf21197a41f663c9b63ddc87fc386722654914c7ee"
            count_num, pass_num, fail_num, error_num = Controller.tag_list[0], Controller.tag_list[1], Controller.tag_list[
                2], Controller.tag_list[3]
            reporturl = Controller.tag_list[4]
            data_markdown = json.dumps({
                "msgtype": "markdown",
                "markdown": {
                    "title": "AutoMagic TestReprot",
                    "text": "![screenshot](http://192.168.110.65/static/images/automagic.png) \n" +
                            ">[AutoMagic TestReprot](http://jenkinsm.acorn-net.com/TestResults/CornerStone/" + reporturl + ") \n\n " +
                            ">总共 " + str(count_num) + " Case，Pass " + str(pass_num) + "，Fail " + str(fail_num) + "，Error " + str(error_num) + "\n"+
                            "运行时间: "+str(exectime)[:-7]
                }
            })
            popautomagic.sendAutoMagic(url, data_markdown)

    @classmethod
    def get_client(cls):
        '''
        获取testrail接口对象
        :return: 返回testrail接口对象
        '''
        if cls.client is None:
            cls.client = testrail.APIClient('http://172.17.3.70/testrail/')
            cls.client.user = cls.user
            cls.client.password = cls.password

        return cls.client

    @classmethod
    def init(cls):
        cls.args = get_args()
        cls.action = Action()
        cls.set_conn()
        cls.start = datetime.datetime.now()
        browser = Controller.args.browser
        Controller.video = Controller.args.video
        if browser is not None:
            Controller.action_test('openBrowser', '', browser, None, None)
        else:
            Controller.action_test('openBrowser', '', 'chrome', None, None)

    @classmethod
    def set_conn(cls):
        cls.conn = MySQLdb.connect(host='172.21.129.32', port=3306, user='automagic', passwd='admin@123', db='autoplat',
                                   charset='utf8')
        cls.cur = cls.conn.cursor()

    @classmethod
    def my_execute(cls, sql):
        try:
            cls.conn.ping()
        except:
            cls.set_conn()

        cls.cur.execute(sql)

    @classmethod
    def action_test(cls, *args):
        action_keyword = cls.action.keyword2action.get(args[0], None)
        if action_keyword is not None:
            # action_object, step_desc, value, loc
            if cls.expand_paras_dict is None:
                # 以非任务方式执行cass
                return action_keyword(cls.action, args[1], args[2], (args[3], args[4]))
            else:
                # 以任务方式执行cass，需要进行扩展参数的替换
                return action_keyword(cls.action, args[1], cls.expand_paras(args[2]), (args[3], args[4]))

        else:
            return u"关键字处理函数未定义！"

    @classmethod
    def set_expand_paras_dict(cls, task_id):
        Controller.my_execute(u'''SELECT codename, codevalue FROM autoplat_codelist WHERE taskid_id = %s''' % task_id)
        expand_paras = Controller.cur.fetchall()
        cls.expand_paras_dict = {}
        for code_name, code_value in expand_paras:
            cls.expand_paras_dict[u'{%s}' % code_name] = code_value

    @classmethod
    def expand_paras(cls, input_text):
        for expand_para in cls.expand_paras_dict:
            input_text = input_text.replace(expand_para, cls.expand_paras_dict[expand_para])
        return input_text

    @classmethod
    def update_result(cls):
        '''
        将测试用例结果更新到数据库
        :return: None
        '''
        case_id_str = ur'(%s)' % ur','.join(unicode(case_id) for case_id in Controller.case_id_list)
        when_list = []
        for idx in xrange(len(Controller.result_list)):
            when_list.append(ur'''WHEN %s THEN "%s"''' % (Controller.case_id_list[idx],
                                                          Controller.result_list[idx].replace('"', "'") + (
                                                          u'\n运行时间：%s' % time.ctime(time.time()))))
        sql_str = ur'''UPDATE autoplat_case SET debuginfo = CASE id %s END WHERE id IN %s''' % (
        u' '.join(when_list), case_id_str)
        Controller.my_execute(sql_str)
        Controller.conn.commit()

    @classmethod
    def update_testrail(cls):
        print u"testrail update start..."
        try:
            client = Controller.get_client()
            for flag_info, result in zip(cls.flag_list, cls.result_list):
                if cls.run_id and cls.user and cls.password and flag_info[0]:
                    para_str = u'add_result_for_case/%s/%s' % (cls.run_id, flag_info[0])
                    try:
                        client.send_post(para_str, {'status_id': flag_info[1], 'comment': result})
                    except Exception, E:
                        print E
        except Exception, e:
            print e
        print u"testrail update end..."


def get_args():
    '''
    解析命令行参数
    :return: 命令行参数命名空间
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', action='store', dest='run_id', type=str, help='Run ID')
    parser.add_argument('-p', action='store', dest='project_id', type=str, help='Project ID')
    parser.add_argument('-c', action='store', dest='case_id', type=str, help='Case ID')
    parser.add_argument('-u', action='store', dest='user_id', type=str, help='User ID')
    parser.add_argument('-t', action='store', dest='task_id', type=str, help='Task ID')
    parser.add_argument('-b', action='store', dest='browser', type=str, help='Browser')
    parser.add_argument('-v', action='store', dest='video', type=str, help='Video True or False')
    parser.add_argument('-d', action='store', dest='popding', type=str, help='ding ding poping')
    rst = parser.parse_args()
    return rst


def gen_test_cass(suite):
    '''
    生成测试用例
    :param suite: 测试用例集对象
    :return:
    '''

    project_id = Controller.args.project_id
    task_id = Controller.args.task_id

    pid_info = u''
    cid_info = u''

    if project_id is not None:
        pid_info = u'AND tb4.projectid_id = %s' % project_id
        case_id = None
    elif task_id is not None:
        # 查询、初始化任务相关的扩展参数
        Controller.set_expand_paras_dict(task_id)

        Controller.run_id = Controller.args.run_id
        user_id = Controller.args.user_id
        if user_id is not None:
            Controller.my_execute(
                u"""SELECT testrailuser, testrailpass FROM autoplat_user WHERE username = '%s'""" % user_id)
            user_info = Controller.cur.fetchall()
            if user_info:
                Controller.user, Controller.password = user_info[0]

        Controller.my_execute(u'''SELECT caselist FROM autoplat_task WHERE id = %s''' % task_id)
        caseid = Controller.cur.fetchall()
        if caseid:
            case_id = caseid[0][0]
        else:
            case_id = '0'
    else:
        case_id = Controller.args.case_id

    if case_id is not None:
        casedict = eval(case_id)
        if type(casedict) is int:
            case_id = case_id
        else:
            case_id = ''
            caselist = {}
            for i in casedict:
                caselist[int(i)] = casedict[i]
            casedict = sorted(caselist.iteritems())
            for i in casedict:
                case_id = case_id + ',' + i[1]
            case_id = case_id[1:]
        cid_info = u'AND tb4.id IN (%s)' % case_id

    Controller.my_execute(u'''SELECT tb4.id, tb4.testrailcaseid, tb4.casedesc, tb6.keyword, tb5.descr, tb5.inputtext, tb7.locmode, tb7.location
                            FROM autoplat_product AS tb1
                            RIGHT JOIN autoplat_project tb2 ON tb2.productid_id = tb1.id
                            RIGHT JOIN autoplat_module tb3 ON tb3.projectid_id = tb2.id
                            RIGHT JOIN autoplat_case AS tb4 ON tb4.moduleid_id = tb3.id
                            RIGHT JOIN autoplat_step AS tb5 ON tb5.caseid_id = tb4.id
                            LEFT JOIN autoplat_keyword AS tb6 ON tb6.id = tb5.keywordid_id
                            LEFT JOIN autoplat_element AS tb7 ON tb7.id = tb5.elementid_id
                            WHERE tb1.isenabled = 1 AND tb2.isenabled = 1 AND tb3.isenabled AND tb4.isenabled = 1
                            %s %s
                            ORDER BY tb3.sortby DESC , tb4.id ASC, tb5.id ASC''' % (pid_info, cid_info))
    case_list = Controller.cur.fetchall()
    # 输出Case步骤
    # for x in case_list:
    #     x = str(x).replace('u\'','\'')
    #     print x.decode("unicode-escape")
    case_flag = None
    step_flag = 0
    test_attr = [int(idx.strip()) for idx in case_id.split(',')] if case_id not in ['', None, 'None'] else []

    # 解析所有case信息，并生成所有的测试用例函数
    for idx, case in enumerate(case_list):
        if case_flag != case[0]:
            if step_flag != idx:
                setattr(TestSuite, 'test_case%d' % case_flag, TestSuite.generateTest(case_list[step_flag:idx]))
                if case_flag in test_attr:
                    test_attr[test_attr.index(case_flag)] = 'test_case%d' % case_flag
                else:
                    test_attr.append('test_case%d' % case_flag)
                step_flag = idx
            case_flag = case[0]
    if case_flag:
        setattr(TestSuite, 'test_case%d' % case[0], TestSuite.generateTest(case_list[step_flag:]))
        if case[0] in test_attr:
            test_attr[test_attr.index(case[0])] = 'test_case%d' % case[0]
        else:
            test_attr.append('test_case%d' % case[0])

    for test_fun in test_attr:
        if type(test_fun) != int:
            suite.addTest(TestSuite(test_fun))


def run_suite():
    suite = unittest.TestSuite()
    gen_test_cass(suite)

    # 获取系统当前时间
    now = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    result = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'result', day)

    # 定义个报告存放路径，支持相对路径
    if not os.path.exists(result):
        os.mkdir(result)

    filename = os.path.join(result, "%s_result.html" % now)

    Controller.tag_list[4] = os.path.join(day, "%s_result.html" % now)

    fp = file(filename, 'wb')

    report_title = u'自动化测试报告'
    if Controller.args.task_id is not None:
        Controller.my_execute(
            u'''SELECT taskname, tasktype FROM autoplat_task WHERE id = %s''' % Controller.args.task_id)
        task_info = Controller.cur.fetchall()
        if task_info:
            report_title = u'%s报告' % task_info[0][0]
            Controller.task_name = task_info[0][0]
            Controller.task_type = task_info[0][1]

    # 定义测试报告
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp, verbosity=1, title=report_title, description=u'用例执行情况：',
                                           result_list=Controller.result_list, tag_list=Controller.tag_list)

    # 运行测试用例
    runner.run(suite)

    # 关闭报告文件
    fp.close()


if "__main__" == __name__:
    # 初始化控制类对象：实例化浏览器实例
    Controller.init()
    try:
        if Controller.args.task_id is not None:
            Controller.my_execute(ur'''UPDATE autoplat_task SET status = 1 WHERE id = %s''' % Controller.args.task_id)
            Controller.conn.commit()

        run_suite()

        Controller.update_result()
        Controller.update_testrail()
    except KeyboardInterrupt:
        run_suite()
    finally:
        # 释放控制类对象信息：关闭浏览器实例
        if Controller.args.task_id is not None:
            Controller.my_execute(ur'''UPDATE autoplat_task SET status = 2 WHERE id = %s''' % Controller.args.task_id)
            Controller.conn.commit()

        Controller.conn.close()

        Controller.conn = None
        Controller.cur = None
        Controller.action = None
        Controller.client = None
        Controller.run_id = None
        del Controller.result_list[:]
        del Controller.case_id_list[:]
        del Controller.flag_list[:]
        if Controller.args.task_id is not None:
            Controller.update_task_history()
