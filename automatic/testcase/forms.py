# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2020-01-06
"""
from django import forms
from automatic.testcase.models import *


class FormCase(forms.ModelForm):
    class Meta:
        model = Case
        fields = ('casedesc','testrailcaseid','projectid','moduleid','isenabled','dependent')


class FormCaseset(forms.ModelForm):
    class Meta:
        model = Caseset
        fields = ('descr', 'caseid', 'isenabled')


class FormStep(forms.ModelForm):
    class Meta:
        model = Step
        fields = ('caseid', 'descr', 'keywordid','elementid','inputtext')