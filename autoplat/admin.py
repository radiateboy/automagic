# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2016-08-03
"""
from django import forms
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# from autoplat.models import User

from autoplat import models

class ProductAdmin(admin.ModelAdmin):
    list_display = (id , 'name', 'isenabled','descr', 'createtime', 'createat','updatetime','updateat')

class ProjectAdmin(admin.ModelAdmin):
    list_display = (id , 'productid','name', 'version', 'isenabled','descr', 'createtime', 'createat','updatetime','updateat')

class ModuleAdmin(admin.ModelAdmin):
    list_display = (id , 'projectid','name', 'isenabled', 'createtime', 'createat','updatetime','updateat')

class CaseAdmin(admin.ModelAdmin):
    list_display = (id , 'moduleid', 'casedesc', 'isenabled','dependent', 'createtime', 'createat','updatetime','updateat')
    search_fields = ('casedesc',)

    def save_model(self, request, obj, form, change):
        if change:  # change
            obj_original = self.model.objects.get(pk=obj.pk)
        else:  # add
            obj_original = None

        obj.user = request.user
        obj.save()

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(CaseAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct

class CasesetAdmin(admin.ModelAdmin):
    list_display = (id , 'descr','isenabled', 'caseid', 'createtime', 'createat','updatetime','updateat')


class ElementAdmin(admin.ModelAdmin):
    list_display = ('moduleid', 'descr', 'locmode', 'location', 'createtime', 'createat','updatetime','updateat')


class StepAdmin(admin.ModelAdmin):
    list_display = ('caseid', 'stepid','descr', 'keywordid', 'elementid', 'inputtext', 'createtime', 'createat','updatetime','updateat')

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username','password','email','mobile','is_active','is_admin','testrailuser','testrailpass')

class UserandProductAdmin(admin.ModelAdmin):
    list_display = ('username', 'productname')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('taskname','tasktype','status','testrailrunid','testsectionid','projectid','caselist','createtime', 'createat','updatetime','updateat')

class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword','kwdescr','createtime', 'createat','updatetime','updateat')

class TaskhistoryAdmin(admin.ModelAdmin):
    list_display = ('taskid', 'userid', 'tasktype', 'taskname', 'case_tag_all', 'case_tag_pass', 'case_tag_fail', 'case_tag_error', 'starttime', 'exectime')

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('email','username', 'password', 'realname','mobile' ,'is_active', 'is_admin','testrailuser','testrailpass')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = ('email','username', 'password', 'realname','mobile' ,'is_active', 'is_admin','testrailuser','testrailpass')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email','username', 'password', 'realname','dept','mobile' ,'is_active', 'is_admin','testrailuser','testrailpass')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email','username', 'password', 'realname','mobile' ,'is_active', 'is_admin','testrailuser','testrailpass')}),
        # ('Personal info', {'fields': ('date_of_birth',)}),
        # ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'realname','dept','email','mobile' ,'is_active', 'is_admin','testrailuser','testrailpass')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()



# Now register the new UserAdmin...
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Module, ModuleAdmin)
admin.site.register(models.Case, CaseAdmin)
admin.site.register(models.Caseset, CasesetAdmin)
admin.site.register(models.Element, ElementAdmin)
admin.site.register(models.Step, StepAdmin)
admin.site.register(models.UserandProduct,UserandProductAdmin)
admin.site.register(models.Keyword, KeywordAdmin)
admin.site.register(models.Task,TaskAdmin)
admin.site.register(models.Taskhistory,TaskhistoryAdmin)
