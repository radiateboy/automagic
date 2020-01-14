# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2020-01-06
"""
from django.db import models
# Create your models here.


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