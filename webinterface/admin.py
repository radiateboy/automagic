from django import forms
from django.contrib import admin
# Register your models here.
from webinterface import models

class WebinterfaceAdmin(admin.ModelAdmin):
    list_display = (id , 'projectid','moduleid', 'descr', 'isenabled','url', 'method')
    search_fields = ('descr',)

    def save_model(self, request, obj, form, change):
        if change:  # change
            obj_original = self.model.objects.get(pk=obj.pk)
        else:  # add
            obj_original = None

        obj.user = request.user
        obj.save()

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(WebinterfaceAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct

class WebresponseAdmin(admin.ModelAdmin):
    list_display = (id , 'webinterfaceid','params', 'exectime', 'expected','actual', 'status_code', 'Response_content')
    search_fields = ('webinterfaceid',)

admin.site.register(models.Webinterface,WebinterfaceAdmin)
admin.site.register(models.Webresponse, WebresponseAdmin)