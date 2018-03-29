# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2017-03-29
"""

from __future__ import unicode_literals

from autoplat.models import *
# Create your models here.

class Webinterface(models.Model):
    Method_Choice = (
        ('POST','post'),
        ('GET','get'),
        ('OPTIONS','options'),
        ('HEAD','head'),
        ('PUT','put'),
        ('PATCH','patch'),
        ('DELETE','delete'),
    )
    projectid = models.ForeignKey(Project)
    moduleid = models.ForeignKey(Module)
    testrailcaseid = models.CharField(max_length=12,null=True, blank=True, editable=True)
    descr = models.CharField(max_length=255, verbose_name="Title")
    isenabled = models.BooleanField(default=True)
    url = models.CharField(max_length=1024, blank=True, editable=True)
    method = models.CharField(max_length=12, choices=Method_Choice, blank=True, editable=True)
    headers = models.CharField(max_length=1024, default=None,null=True, blank=True, editable=True)
    cookies = models.CharField(max_length=1024, default=None,null=True, blank=True, editable=True)
    data = models.TextField(null=True, blank=True, default=None,editable=True)
    files = models.CharField(max_length=1024, default=None,null=True, blank=True, editable=True)
    auth = models.CharField(max_length=1024, default=None,null=True, blank=True, editable=True)
    timeout = models.CharField(max_length=8, default=None,null=True, blank=True, editable=True)
    allow_redirects = models.CharField(max_length=1024, default=None,null=True, blank=True, editable=True)
    proxies = models.CharField(max_length=1024, default=None,null=True, blank=True, editable=True)
    verify = models.CharField(max_length=1024, default=None,null=True, blank=True, editable=True)
    stream = models.CharField(max_length=1024, default=None,null=True, blank=True, editable=True)
    cert = models.CharField(max_length=1024, default=None,null=True, blank=True, editable=True)
    debuginfo = models.TextField(null=True, blank=True, editable=True)
    createtime = models.DateTimeField(auto_now_add=True)
    createat = models.CharField(max_length=32,null=True, blank=True, editable=True)
    updatetime = models.DateTimeField(auto_now_add=True)
    updateat = models.CharField(max_length=32,null=True, blank=True, editable=True)

    def __unicode__(self):
        return self.descr

class Webresponse(models.Model):
    webinterfaceid = models.ForeignKey(Webinterface)
    params = models.TextField(null=True, blank=True, editable=True)
    exectime = models.CharField(max_length=16, null=False, blank=True)
    expected = models.CharField(max_length=255, null=True, blank=True, editable=True)
    actual = models.CharField(max_length=255, null=True, blank=True, editable=True)
    status_code = models.CharField(max_length=4,null=False, blank=True)
    Response_content = models.TextField(blank=True)
    createtime = models.DateTimeField(auto_now_add=True)
    createat = models.CharField(max_length=32,null=True, blank=True, editable=True)
    updatetime = models.DateTimeField(auto_now_add=True)
    updateat = models.CharField(max_length=32,null=True, blank=True, editable=True)

    def __unicode__(self):
        return str(self.id)