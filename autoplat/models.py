# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2016-08-03
"""
from __future__ import unicode_literals

import datetime

from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=32, verbose_name='产品名称', unique=True)
    # version = models.CharField(max_length=32)
    isenabled = models.BooleanField(default=True, blank=True, verbose_name='产品状态')
    descr = models.TextField(null=True, blank=True, verbose_name='产品描述')
    createtime = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='创建时间')
    createat = models.CharField(max_length=32, null=True, blank=True, editable=True, verbose_name='创建者')
    updatetime = models.DateTimeField(auto_now=True,null=True, blank=True, verbose_name='更新时间')
    updateat = models.CharField(max_length=32, null=True, blank=True, editable=True, verbose_name='更新者')
    sortby = models.IntegerField(null=True, blank=True, editable=True, default=0, verbose_name='排序')

    def __unicode__(self):
        return  self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.createtime = datetime.datetime.now()
            self.updatetime = datetime.datetime.now()

        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-sortby"]

class Project(models.Model):
    productid = models.ForeignKey(Product, verbose_name='产品名称')
    name = models.CharField(max_length=32, unique=True, verbose_name='项目名称')
    version = models.CharField(max_length=32, null=True, blank=True, editable=True, verbose_name='版本')
    isenabled = models.BooleanField(default=True, verbose_name='状态')
    descr = models.TextField(null=True, blank=True, editable=True,verbose_name='项目描述')
    createtime = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True,verbose_name='创建时间')
    createat = models.CharField( max_length=32, null=True, blank=True, editable=True, verbose_name='创建者')
    updatetime = models.DateTimeField(auto_now=True,null=True, blank=True, verbose_name='更新时间')
    updateat = models.CharField(max_length=32, null=True, blank=True, editable=True, verbose_name='更新者')
    sortby = models.IntegerField(null=True, blank=True, editable=True, default=0, verbose_name='排序')

    def __unicode__(self):
        return  self.name

    class Meta:
        ordering = ["-sortby"]

class Module(models.Model):
    projectid = models.ForeignKey(Project, verbose_name='所属项目')
    name = models.CharField(max_length=32, verbose_name='模块名称')
    isenabled = models.BooleanField(default=True, verbose_name='状态')
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    createat = models.CharField(max_length=32 ,null=True, blank=True, editable=True, verbose_name='创建者')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    updateat = models.CharField(max_length=32, null=True, blank=True, editable=True, verbose_name='更新者')
    sortby = models.IntegerField(null=True, blank=True, editable=True, default=0, verbose_name='排序')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["-sortby"]

class Keyword(models.Model):
    productid = models.IntegerField(verbose_name='所属产品', null=True, blank=True, editable=True)
    keyword = models.CharField(max_length=32, unique=True)
    kwdescr = models.TextField(null=True,blank=True,editable=True)
    createtime = models.DateTimeField(auto_now_add=True)
    createat = models.CharField(max_length=32, null=True, blank=True, editable=True)
    updatetime = models.DateTimeField(auto_now=True)
    updateat = models.CharField(max_length=32, null=True, blank=True, editable=True)

    def __unicode__(self):
        return self.keyword

    class Meta:
        ordering = ["productid"]

class Element(models.Model):
    Element_Choice = (
        ('id','id'),
        ('name','name'),
        ('css selector','css selector'),
        ('xpath','xpath'),
        ('class_name','class name'),
        ('tag_name','tag name'),
        ('link_text','link text'),
        ('portial_link_text','portial link text')
    )
    projectid = models.ForeignKey(Project,editable=True)
    moduleid = models.ForeignKey(Module, editable=True)
    descr = models.CharField(max_length=100, editable=True)
    locmode = models.CharField(max_length=32, choices=Element_Choice, null=True, blank=True, editable=True)
    location = models.CharField(max_length=200, null=True, blank=True, editable=True)
    createtime = models.DateTimeField(auto_now_add=True)
    createat = models.CharField(max_length=32, null=True, blank=True, editable=True)
    updatetime = models.DateTimeField(auto_now=True)
    updateat = models.CharField(max_length=32, null=True, blank=True, editable=True)

    def __unicode__(self):
        return self.descr

class Case(models.Model):
    projectid = models.ForeignKey(Project)
    moduleid = models.ForeignKey(Module)
    testrailcaseid = models.CharField(max_length=12,null=True, blank=True, editable=True)
    casedesc = models.CharField(max_length=255, verbose_name="Title")
    isenabled = models.BooleanField(default=True)
    issmoke = models.BooleanField(default=False)
    dependent = models.CharField(max_length=8,null=True, blank=True, editable=True)
    debuginfo = models.CharField(max_length=9999, null=True, blank=True, editable=True)
    createtime = models.DateTimeField(auto_now_add=True)
    createat = models.CharField(max_length=32,null=True, blank=True, editable=True)
    updatetime = models.DateTimeField(auto_now_add=True)
    updateat = models.CharField(max_length=32,null=True, blank=True, editable=True)

    def __unicode__(self):
        return self.casedesc

class Caseset(models.Model):
    descr = models.CharField(max_length=200)
    caseid = models.CharField(validators=[validate_comma_separated_integer_list],max_length=255)
    isenabled = models.BooleanField(default=True)
    createtime = models.DateTimeField(auto_now_add=True)
    createat = models.CharField(max_length=32, null=True, blank=True, editable=True)
    updatetime = models.DateTimeField(auto_now=True)
    updateat = models.CharField(max_length=32, null=True, blank=True, editable=True)

    def __unicode__(self):
        return self.descr

class Step(models.Model):
    caseid = models.ForeignKey(Case)
    stepid = models.IntegerField(null=True, blank=True, editable=True)
    descr = models.CharField(max_length=200, null=True, blank=True, editable=True)
    keywordid = models.ForeignKey(Keyword)
    elementid = models.ForeignKey(Element,null=True, blank=True)
    inputtext = models.CharField(max_length=200, null=True, blank=True, editable=True)
    createtime = models.DateTimeField(auto_now_add=True)
    createat = models.CharField(max_length=32, null=True, blank=True, editable=True)
    updatetime = models.DateTimeField(auto_now=True)
    updateat = models.CharField(max_length=32, null=True, blank=True, editable=True)

    def __unicode__(self):
        return  self.descr

class MyUserManager(BaseUserManager):
    # def current_time(self):
    #     """get current time """
    #     from datetime import datetime
    #     return datetime.now().strftime("%Y-%m-%d")

    def create_user(self, username, email, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        if not username:
            raise ValueError('username is unique')
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, password.
        """
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    Dept_Choice = (
        ('测试', '测试'),
        ('开发', '开发'),
    )
    username = models.CharField(max_length=50, verbose_name="username", unique=True, null=True)
    password = models.CharField(('password'), max_length=128)
    realname = models.CharField(max_length=50, verbose_name="真实姓名", null=True, blank=True, editable=True)
    mobile = models.CharField(max_length=11, verbose_name="Phone Number", null=True, blank=True, editable=True)
    email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True)
    dept = models.CharField(verbose_name=u'部门',choices=Dept_Choice, max_length=100)
    is_active = models.BooleanField(default=True, verbose_name='激活状态')
    is_admin = models.BooleanField(default=False, verbose_name='是否管理员')
    testrailuser = models.CharField(max_length=50, verbose_name="TestRail用户名", null=True,blank=True, editable=True)
    testrailpass = models.CharField(max_length=50, verbose_name="TestRail密码", null=True,blank=True, editable=True)
    objects = MyUserManager()
    base_objects = BaseUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __unicode__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserandProduct(models.Model):
    username = models.ForeignKey(User)
    productname = models.ForeignKey(Product)



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
    projectid = models.ForeignKey(Project)
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
    taskid = models.ForeignKey(Task)
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
    taskid = models.ForeignKey(Task)
    userid = models.ForeignKey(User)
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