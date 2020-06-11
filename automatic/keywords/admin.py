from django.contrib import admin

# Register your models here.

from automatic.keywords import models


class KeywordAdmin(admin.ModelAdmin):
    list_display = (id, 'keyword', 'kwdescr','createat', 'createtime', 'updateat', 'updatetime')
    search_fields = ('keyword', 'kwdescr')


admin.site.register(models.Keyword, KeywordAdmin)