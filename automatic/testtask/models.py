# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2020-01-06
"""
from django.db import models
from automatic.management.models import Project, User
# Create your models here.


class Task(models.Model):
    Task_Choice = (
        ('1', '执行用例'),
        ('2', '用例同步'),
        ('3', '关联Jenkins'),
    )
    taskname = models.CharField(max_length=255,verbose_name="任务描述")
    tasktype = models.CharField(max_length=32, choices=Task_Choice, blank=True, editable=True)
    status = models.SmallIntegerField(default=0, verbose_name='任务状态')
    issmoke = models.BooleanField(default=False)
    testrailsuites = models.CharField(max_length=8, verbose_name='TestRail测试集ID', null=True, blank=True, editable=True)
    testrailrunid = models.CharField(max_length=8,verbose_name='TestRail执行ID',null=True,blank=True, editable=True)
    testsectionid = models.CharField(max_length=8, verbose_name='TestRail用例节点ID',null=True,blank=True, editable=True)
    projectid = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    jenkins_server_url = models.CharField(max_length=100, verbose_name='JenkinsServer', null=True, blank=True, editable=True)
    user_id = models.CharField(max_length=32, verbose_name='JenkinsUserid', null=True, blank=True, editable=True)
    api_token = models.CharField(max_length=32, verbose_name='JenkinsApitoken', null=True, blank=True, editable=True)
    build_name = models.CharField(max_length=32, verbose_name='JenkinsBuildName', null=True, blank=True, editable=True)
    caselist = models.CharField(max_length=10240, verbose_name='用例列表')
    createtime = models.DateTimeField(auto_now_add=True)
    createat = models.CharField(max_length=32, null=True, blank=True, editable=True)
    updatetime = models.DateTimeField(auto_now=True)
    updateat = models.CharField(max_length=32, null=True, blank=True, editable=True)

    def __unicode__(self):
        return  self.taskname

class Codelist(models.Model):
    taskid = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    codename = models.CharField(max_length=32)
    codedescr = models.CharField(max_length=255)
    codevalue = models.CharField(max_length=255)
    createtime = models.DateTimeField(auto_now_add=True)
    createat = models.CharField(max_length=32, null=True, blank=True, editable=True)
    updatetime = models.DateTimeField(auto_now=True)
    updateat = models.CharField(max_length=32, null=True, blank=True, editable=True)

    def __unicode__(self):
        return self.codename

class Taskhistory(models.Model):
    taskid = models.ForeignKey(Task, on_delete=models.DO_NOTHING)
    userid = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    tasktype = models.CharField(max_length=32, blank=True, editable=True)
    taskname = models.CharField(max_length=255, verbose_name="任务描述")
    case_tag_all = models.CharField(max_length=8, null=True, blank=True, editable=True)
    case_tag_pass = models.CharField(max_length=8, null=True, blank=True, editable=True)
    case_tag_fail = models.CharField(max_length=8, null=True, blank=True, editable=True)
    case_tag_error = models.CharField(max_length=8, null=True, blank=True, editable=True)
    starttime = models.DateTimeField(blank=True, editable=True)
    exectime = models.CharField(max_length=32, null=True, blank=True, editable=True)
    reporturl = models.CharField(max_length=255, verbose_name="report Url", null=True)
    build_name = models.CharField(max_length=32, null=True, blank=True, editable=True)
    build_number = models.CharField(max_length=8, null=True, blank=True, editable=True)

    def __unicode__(self):
        return self.pk