from django.contrib import admin

# Register your models here.

from automatic.element import models


class ElementAdmin(admin.ModelAdmin):
    list_display = (id, 'descr', 'projectid', 'moduleid', 'locmode', 'location', 'createat', 'createtime', 'updateat', 'updatetime')
    search_fields = ('keyword', 'kwdescr')


admin.site.register(models.Element, ElementAdmin)