# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2016-08-03
"""
from rest_framework import serializers
from autoplat.models import *

#Product
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'isenabled', 'descr')

#Project
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'isenabled', 'descr','productid')


#Module
class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'name', 'isenabled', 'projectid')


#Keyword
class KeywordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'keyword', 'kwdescr', 'productid')


#Element
class ElementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Element
        fields = ('id', 'descr', 'locmode', 'location','projectid','moduleid')


#Case
class CaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Case
        fields = ('id', 'casedesc', 'projectid', 'moduleid','testrailcaseid')



#Step
class StepSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Step
        fields = ('caseid', 'descr', 'keywordid', 'elementid','inputtext')
