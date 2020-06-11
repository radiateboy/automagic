from django.contrib import admin

# Register your models here.

from automatic.management import models


class ProductAdmin(admin.ModelAdmin):
    list_display = (id, 'name', 'isenabled', 'descr','createat', 'createtime', 'updateat', 'updatetime')
    search_fields = ('name','descr')


class ProjectAdmin(admin.ModelAdmin):
    list_display = (id, 'name', 'isenabled','version','descr','createat', 'createtime', 'updateat', 'updatetime')
    search_fields = ('name','descr','version')


class ModuleAdmin(admin.ModelAdmin):
    list_display = (id, 'name', 'isenabled', 'createat', 'createtime', 'updateat', 'updatetime')
    search_fields = ('name',)


admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Module, ModuleAdmin)