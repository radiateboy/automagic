from django.contrib import admin

# Register your models here.

from automatic.testcase import models


class CaseAdmin(admin.ModelAdmin):
    list_display = (id, 'casedesc', 'isenabled','issmoke', 'projectid', 'createat', 'createtime', 'updateat', 'updatetime')
    search_fields = ('casedesc', 'projectid')


class CasesetAdmin(admin.ModelAdmin):
    list_display = (id, 'descr', 'caseid', 'isenabled', 'createat', 'createtime', 'updateat', 'updatetime')
    search_fields = ('descr',)


class StepAdmin(admin.ModelAdmin):
    list_display = (id, 'caseid', 'stepid', 'descr', 'keywordid', 'elementid', 'inputtext')
    search_fields = ('caseid',)


admin.site.register(models.Case, CaseAdmin)
admin.site.register(models.Caseset, CasesetAdmin)
admin.site.register(models.Step, StepAdmin)