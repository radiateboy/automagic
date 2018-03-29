# Seleniumkeyword介绍 #

seleniumkword是客户端执行脚本，AutoMagic的执行效果展示主要靠它来体现，它的执行依附于web平台存储的用例和场景数据，seleniumkeyword可以不需要部署在服务器端，只要它能够连接到服务器端的数据库，在本地部署即可执行。（这样也方便我们做分布式执行测试用例）

## 安装运行环境 ##

在安装python、selenium、 mysqldb 的环境下运行

## 目录脚本说明 ##

**TestSuite.py  测试用例执行脚本引擎是 ，它可以通过参数实现不同的执行方式**

>-t  [taskid]    指定执行的AutoMagic任务

>-u  [userid]    指定执行脚本的用户

>-r  [runid]     执行测试用例脚本要同步的TestRailRunid，它只有在执行 -t 参数时才会生效。

>-c  [caseid]    指定要执行的单个用例的编号

>-p  [projectid] 指定要执行的项目id，会依次执行项目中所有模块和用例状态是启用的所有用例

>-b  [browser]   指定执行用例过程所使用浏览器，默认使用chrome浏览器,也可在执行case过程中通过openbrowser关键字重置

>-v  [1] 指定是否启用录屏功能（仅支持Linux系统，需要安装recordmydesktop录屏软件）

>-d  [1] 钉钉消息接口，启用后可以将测试结果发送的钉钉群中

Exp:

``` python TestSuite.py -t 1 -u tsbc -r 1433 -b chrome -v 1```

**CustomKeyword.py  是我们自定义关键字维护脚本。**

>自定义关键字示例：
```python
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
    action_object.send_keys(loc, value)
```

**AddCase.py 同步用例到TestRail到脚本**

>-t  [taskid]    指定执行同步的AutoMagic任务

>-u  [userid]    指定执行脚本的用户

>-s  [sctionid]     执行同步case到TestRail的那个用例集（section_id代表所在用例集）

**HTMLTestRunner.py 生成报告的脚本文件**

**RestApiUtil.py、RestApiUtil.py 是发包MW模拟安全事件和发送pcap发包接口**

**testrail.py TestRail的接口API**

**result目录： 为报告接口目录**
>在生成的每日报告目录中会生成用例执行过程日志文件

**data目录： 执行上传附件关键字，附件存放目录**

**sendlog目录： 通过tcp、udp 514 发送Syslog 的应用**

