from django.contrib import admin

# Register your models here.

from automatic.testtask import models


class KeywordAdmin(admin.ModelAdmin):
    list_display = (id, 'taskname', 'tasktype','status', 'issmoke', 'createat', 'createtime', 'updateat', 'updatetime')
    search_fields = ('taskname', 'tasktype')


class CodelistAdmin(admin.ModelAdmin):
    list_display = (id, 'codename', 'codedescr', 'codevalue', 'createat', 'createtime', 'updateat', 'updatetime')
    search_fields = ('codename',)


class TaskhistoryAdmin(admin.ModelAdmin):
    list_display = (id, 'taskid', 'tasktype', 'taskname', 'case_tag_all', 'case_tag_pass', 'case_tag_fail', 'case_tag_error')
    search_fields = ('taskid', 'taskname')


admin.site.register(models.Task, KeywordAdmin)
admin.site.register(models.Codelist, CodelistAdmin)
admin.site.register(models.Taskhistory, TaskhistoryAdmin)