# -*- coding:utf-8 -*-
from pprint import pprint

__author__ = 'ray'

import testrail

client = testrail.APIClient('http://172.17.3.70/testrail/')
client.user = 'jiangpeng.chen@acorn-net.com'
client.password = '123qwe'

"""  更新Testrun 结果

add_result_for_case/[runid]/[caseid]
status_id:
{
  1 : Passed
  4 : Retest
  5 : Failed
}

"""
result = client.send_post(
    'add_result_for_case/1047/1036925',
    {'status_id': 1, 'comment': 'AutoMagic Flag.' }
)
# pprint(result)


"""  获取用例信息

get_case/[caseid]
"""
case = client.send_get('get_case/1036925')
# pprint(case)


"""  获取用例节点信息

"""
section = client.send_get('get_section/45752')
# pprint(section)


""" 添加测试用例
send_post('add_case/[sectionid]',casedata)
"""
casedata = {
    "title":"AutoMagic 测试使用admin用户登录。",
    "template_id":"1",
    "type_id":"1",
    "priority_id":"4",
    "custom_caseversion_id":"8",
    "custom_automation_status":"2",
    "custom_steps": "Step1 跳转到登录页面：http://192.168.110.111\n Step2 输入登录用户名 admin \n Step3 输入登录密码 admin@123\n Step4 点击登录按钮"
}
add_case = client.send_post('add_case/45752',casedata)
# pprint(add_case)


update_case = client.send_post('update_case/1107930',casedata)
pprint(update_case)