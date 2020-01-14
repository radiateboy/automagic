# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2020-01-06
"""
from django.db import models
from automatic.management.models import Project, Module
from automatic.keywords.models import Keyword
from automatic.element.models import Element
from django.core.validators import validate_comma_separated_integer_list
# Create your models here.


class Case(models.Model):
    projectid = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    moduleid = models.ForeignKey(Module, on_delete=models.DO_NOTHING)
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
    caseid = models.ForeignKey(Case, on_delete=models.CASCADE)
    stepid = models.IntegerField(null=True, blank=True, editable=True)
    descr = models.CharField(max_length=200, null=True, blank=True, editable=True)
    keywordid = models.ForeignKey(Keyword, on_delete=models.DO_NOTHING)
    elementid = models.ForeignKey(Element,null=True, blank=True, on_delete=models.DO_NOTHING)
    inputtext = models.CharField(max_length=200, null=True, blank=True, editable=True)
    createtime = models.DateTimeField(auto_now_add=True)
    createat = models.CharField(max_length=32, null=True, blank=True, editable=True)
    updatetime = models.DateTimeField(auto_now=True)
    updateat = models.CharField(max_length=32, null=True, blank=True, editable=True)

    def __unicode__(self):
        return  self.descr
