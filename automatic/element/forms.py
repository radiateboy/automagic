# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2020-01-08
"""
from django import forms
from automatic.element.models import Element
from django.forms import ModelForm, Textarea, Select, TextInput


class FormElement(forms.ModelForm):
    class Meta:
        model = Element
        fields = ('descr','projectid','moduleid','locmode','location')
        widgets = {'locmode': Select(attrs={'class':'ak-left ac-aselect','required':''}),
                   'descr':TextInput(attrs={'class':'form-control','placeholder':'请输入元素描述','required':''}),
                   'location': TextInput(attrs={'class': 'form-control','placeholder':'（如：id_username）','required':''}),
                   }