# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2020-01-06
"""
from __future__ import unicode_literals

import datetime
from django.db import models
from auto_auth.models import User
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
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.createtime = datetime.datetime.now()
            self.updatetime = datetime.datetime.now()

        super(Product, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-sortby"]


class Project(models.Model):
    productid = models.ForeignKey(Product, verbose_name='产品名称', on_delete=models.CASCADE)
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
        return self.name

    class Meta:
        ordering = ["-sortby"]


class Module(models.Model):
    projectid = models.ForeignKey(Project, verbose_name='所属项目', on_delete=models.CASCADE)
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

class UserAndProduct(models.Model):
    username = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    productname = models.ForeignKey(Product, on_delete=models.DO_NOTHING)



