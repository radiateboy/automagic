# -*- coding: utf-8 -*-

import argparse
import testrail
import MySQLdb


def get_args():
    '''
    获取命令行参数
    :return: 命令行参数命名空间
    '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', action='store', dest='user_id', type=str, help='User ID')
    parser.add_argument('-t', action='store', dest='task_id', type=str, help='Task ID')
    parser.add_argument('-s', action='store', dest='section_id', type=str, help='Section ID')
    rst = parser.parse_args()
    return rst


def add_cass(user, password, section_id, case_data):
    '''
    增加testrail测试用例
    :param user: testrail用户名
    :param password: testrail密码
    :param case_data: 需要添加的case
    :return: None
    '''

    client = testrail.APIClient('http://172.17.3.70/testrail/')
    client.user = user
    client.password = password

    result = []
    try:
        for case_id, testrailcaseid, data in case_data:
            if testrailcaseid not in ('', None, 'None'):
                client.send_post('update_case/%s' % testrailcaseid, data)
            else:
                testrailcaseid_new = client.send_post('add_case/%s' % section_id, data).get('id', '')
                result.append((case_id, testrailcaseid_new))
    except Exception, e:
        print e
    finally:
        return result


class MyPySql(object):
    def __init__(self):
        self.conn = None
        self.cur = None
        self.set_conn()

    def set_conn(self):
        self.conn = MySQLdb.connect(host='172.21.129.32', port=3306, user='automagic', passwd='admin@123', db='autoplat', charset='utf8')
        self.cur = self.conn.cursor()

    def execute(self, sql):
        try:
            self.conn.ping()
        except:
            self.set_conn()

        self.cur.execute(sql)

    def fetchall(self):
        return self.cur.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


if "__main__" == __name__:

    my_py_sql = MyPySql()
    args = get_args()

    user = None
    password = None
    case_ids = None

    my_py_sql.execute(ur'''UPDATE autoplat_task SET status = 1 WHERE id = %s''' % args.task_id)
    my_py_sql.commit()

    if args.user_id is not None and args.task_id is not None:
        # 获取用户对应的testrail用户名和密码
        my_py_sql.execute(u"""SELECT testrailuser, testrailpass FROM autoplat_user WHERE username = '%s'""" % args.user_id)
        user_info = my_py_sql.fetchall()
        if user_info:
            user, password = user_info[0]

        # 获取任务对应的case_id
        my_py_sql.execute(u'''SELECT caselist FROM autoplat_task WHERE id = %s''' % args.task_id)
        case_info = my_py_sql.fetchall()
        
        if case_info:
            case_ids = case_info[0][0]
        if case_ids is not None:
            casedict = eval(case_ids)
            if type(casedict) is int:
                case_ids = case_ids
            else:
                case_ids = ''
                for i in casedict:
                    case_ids = case_ids + ',' + casedict[i]
                case_ids = case_ids[1:]

    if user is not None and password is not None and case_ids is not None:
        # 获取所有case的详细信息
        my_py_sql.execute(u'''SELECT tb2.id, tb2.casedesc, tb1.descr, tb2.testrailcaseid
                    FROM autoplat_step AS tb1 LEFT JOIN autoplat_case AS tb2 ON tb1.caseid_id = tb2.id
                    WHERE tb1.caseid_id IN (%s) ORDER BY tb1.caseid_id, tb1.id ''' % case_ids)
        case_info = my_py_sql.fetchall()

        case_data = []
        tmp_id = None
        data = {}
        step_num = 1
        for item in case_info:
            case_id, case_desc, step_desc, testrailcaseid = item
            if tmp_id != case_id:
                tmp_id = case_id
                step_num = 1
                data = {"title": u'%s:%s' % (case_id, case_desc),
                        "template_id": u'1',
                        "type_id": u'1',
                        "priority_id": u'4',
                        "custom_caseversion_id": u'8',
                        "custom_automation_status": u'2',
                        "custom_steps": u'step_%s %s' % (step_num, step_desc)}
                case_data.append([case_id, testrailcaseid, data])
                step_num += 1
            else:
                data['custom_steps'] = u'%s\nstep_%s %s' % (data['custom_steps'], step_num, step_desc)
                step_num += 1

        # 同步所有用例到testrail
        add_result = []
        if case_data:
            add_result = add_cass(user, password, args.section_id, case_data)

        if add_result:
            when_list = []
            for result in add_result:
                when_list.append(ur'''WHEN %s THEN "%s"''' % result)

            sql_str = ur'''UPDATE autoplat_case SET testrailcaseid = CASE id %s END WHERE id in (%s)''' % (ur' '.join(when_list), case_ids)
            my_py_sql.execute(sql_str)
            my_py_sql.commit()

    my_py_sql.execute(ur'''UPDATE autoplat_task SET status = 2 WHERE id = %s''' % args.task_id)
    my_py_sql.commit()
    my_py_sql.close()

