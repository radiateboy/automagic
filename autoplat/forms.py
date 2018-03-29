# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2016-08-05
"""
from django import forms
from autoplat.models import *
from django.forms import ModelForm, Textarea, Select, TextInput

class FormProduct(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name','isenabled','descr','sortby')

class FormProject(forms.ModelForm):

    # inenabled = forms.BooleanField()
    class Meta:
        model = Project
        fields = ('productid','name','isenabled','version','descr','sortby')
        widgets = {'productid': Select(attrs={'class': 'ak-left ac-aselect'})}

class FormModule(forms.ModelForm):

    class Meta:
        model = Module
        fields = ('projectid','name','isenabled','sortby')


class FormElement(forms.ModelForm):

    class Meta:
        model = Element
        fields = ('descr','projectid','moduleid','locmode','location')
        widgets = {'locmode': Select(attrs={'class':'ak-left ac-aselect','required':''}),
                   'descr':TextInput(attrs={'class':'form-control','placeholder':'请输入元素描述','required':''}),
                   'location': TextInput(attrs={'class': 'form-control','placeholder':'（如：id_username）','required':''}),
                   }

class FormCase(forms.ModelForm):

    class Meta:
        model = Case
        fields = ('casedesc','testrailcaseid','projectid','moduleid','isenabled','dependent')
        # widgets = {
        #     'isenabled':forms.TextInput(attrs={'class': 'onoffswitch-checkbox'}),
        # }

class FormKeyword(forms.ModelForm):

    class Meta:
        model = Keyword
        fields = ('keyword','kwdescr')

class FormCaseset(forms.ModelForm):
    class Meta:
        model = Caseset
        fields = ('descr', 'caseid', 'isenabled')

class FormStep(forms.ModelForm):
    class Meta:
        model = Step
        fields = ('caseid', 'descr', 'keywordid','elementid','inputtext')