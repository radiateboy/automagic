# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2020-01-06
"""
from django.db import models
from automatic.management.models import Project, Module
# Create your models here.

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
    projectid = models.ForeignKey(Project, editable=True, on_delete=models.DO_NOTHING)
    moduleid = models.ForeignKey(Module, editable=True, on_delete=models.DO_NOTHING)
    descr = models.CharField(max_length=100, editable=True)
    locmode = models.CharField(max_length=32, choices=Element_Choice, null=True, blank=True, editable=True)
    location = models.CharField(max_length=200, null=True, blank=True, editable=True)
    createtime = models.DateTimeField(auto_now_add=True)
    createat = models.CharField(max_length=32, null=True, blank=True, editable=True)
    updatetime = models.DateTimeField(auto_now=True)
    updateat = models.CharField(max_length=32, null=True, blank=True, editable=True)

    def __unicode__(self):
        return self.descr