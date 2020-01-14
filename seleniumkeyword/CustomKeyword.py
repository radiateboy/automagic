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
#				  value(需要输入的值，多个输入值用逗号隔开), loc(元素的定位信息)
# 函数正常退出时不能有返回值（使用默认的返回值None），出错时返回字符串（记录出错信息）
################################################################################



##############################################################################################
#																							 #
#								 自定义关键字  START									         #
#																							 #
##############################################################################################

@Action.add_action('keau1000_login')
def action_login(action_object, step_desc, value, loc):
	"""
	构造登录使用的公用方法
	"""
	print(value)
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
def action_reset(action_object, step_desc, value, loc):
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
	for i in range(180):
		print(i + 1,)
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
	for i in range(180):
		print(i + 1,)
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
		print("reset succesful.")
	else:
		return "reset failed!"

#																							 #
#								 自定义关键字  END									         #
##############################################################################################
