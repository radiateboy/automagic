from django.contrib import admin

# Register your models here.

from automatic.testcase import models


class CaseAdmin(admin.ModelAdmin):
    list_display = (id, 'casedesc', 'isenabled','issmoke', 'projectid', 'createat', 'createtime', 'updateat', 'updatetime')
    search_fields = ('casedesc', 'projectid')


class StepAdmin(admin.ModelAdmin):
    list_display = (id, 'caseid', 'stepid', 'descr', 'keywordid', 'elementid', 'inputtext')
    search_fields = ('descr',)


admin.site.register(models.Case, CaseAdmin)
admin.site.register(models.Step, StepAdmin)