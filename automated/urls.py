# -*- coding:utf-8 -*-
"""automated URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login,logout
# from django.conf import settings
from autoplat import views as automate
from webinterface import views as interface
# from deviceapp import views as devicemgt

from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf.

router = routers.DefaultRouter()
router.register(r'product', automate.ProductViewSet)
router.register(r'project', automate.ProjectViewSet)
router.register(r'module', automate.ModuleViewSet)
router.register(r'keyword', automate.KeywordViewSet)
router.register(r'element', automate.ElementViewSet)
router.register(r'case', automate.CaseViewSet)
router.register(r'step', automate.StepViewSet)


admin.autodiscover()
urlpatterns = [
    url(r'^test/$', automate.comingsoon, name='test'),
    url(r'^login', login),
    url(r'^logout', logout, {'next_page': '/login/'}),
    url(r'^func/case/add/$', automate.add_case, name='caseadd'),
    url(r'^func/case/list/$|^$|^index/$', login_required(automate.CaseListIndex.as_view()), name='caselist'),
    url(r'^func/case/view/(?P<id>\d+)/$', automate.view_case, name='caseview'),
    url(r'^func/case/update/(?P<id>\d+)/$', automate.update_case, name='caseupdate'),
    url(r'^func/case/copy/(?P<id>\d+)/$', automate.copy_case, name='copycase'),
    url(r'^func/case/del/(?P<id>\d+)/$', automate.del_case, name='casedel'),
    url(r'^func/case/run/$', automate.run_case, name='runcase'),
    url(r'^func/get/caselist/$', automate.get_caselist, name='getcase'),
    url(r'^func/step/del/(?P<id>\d+)/$', automate.del_step, name='stepdel'),
    url(r'^func/element/list/$', login_required(automate.ElementListIndex.as_view()), name='elementlist'),
    url(r'^func/element/add/$', automate.add_element, name='elementadd'),
    url(r'^func/element/update/$', automate.update_element, name='elementupdate'),
    url(r'^func/element/del/(?P<id>\d+)/$', automate.del_element, name='elementdel'),
    url(r'^func/keyword/list/$', login_required(automate.KeyWordListIndex.as_view()), name='keywordlist'),
    url(r'^func/keyword/add/$', automate.add_keyword, name='keywordadd'),
    url(r'^func/keyword/update/$', automate.update_keyword, name='keywordupdate'),
    url(r'^func/keyword/del/(?P<id>\d+)/$', automate.del_keyword, name='keyworddel'),
    url(r'^func/get/keyword/$', automate.get_keyword, name='getkeyword'),
    url(r'^func/get/element/$', automate.get_element, name='getelement'),
    url(r'^func/setedit/element/$', automate.set_edit_element, name='seteditelement'),
    url(r'^func/setedit/keyword/$', automate.set_edit_keyword, name='seteditelement'),
    url(r'^func/task/add/$', automate.add_task, name='taskadd'),
    url(r'^func/task/list/$', login_required(automate.TaskListIndex.as_view()), name='tasklist'),
    url(r'^func/setTree/task/$', automate.set_tree_task, name='settreetask'),
    url(r'^func/task/update/(?P<id>\d+)/$', automate.update_task, name='taskupdate'),
    url(r'^func/task/del/(?P<id>\d+)/$', automate.del_task, name='taskdel'),
    url(r'^func/task/run/$', automate.run_task, name='runtask'),
    url(r'^func/get/taskhistory/$', automate.get_task_history, name='gettaskhistroy'),
    url(r'^setting/user/add/$', automate.add_user, name='adduser'),
    url(r'^setting/user/list/$', login_required(automate.UserListIndex.as_view()), name='userlist'),
    url(r'^setting/user/update/$', automate.update_user, name='userupdate'),
    url(r'^setting/user/del/(?P<id>\d+)/$', automate.del_user, name='userdel'),
    url(r'^setting/product/add/$', automate.add_product, name='productadd'),
    url(r'^setting/product/view/(?P<id>\d+)', automate.view_product, name='productview'),
    url(r'^setting/product/list/$', login_required(automate.ProductListIndex.as_view()), name='productlist'),
    url(r'^setting/product/update/$', automate.update_product, name='productupdate'),
    url(r'^setting/product/del/(?P<id>\d+)/$', automate.del_product, name='productdel'),
    url(r'^setting/project/add/$', automate.add_project, name='projectadd'),
    url(r'^setting/project/list/$', login_required(automate.ProjectListIndex.as_view()), name='projectlist'),
    url(r'^setting/project/view/(?P<id>\d+)', automate.view_project, name='projectview'),
    url(r'^setting/project/update/$', automate.update_project, name='projectupdate'),
    url(r'^setting/project/del/(?P<id>\d+)/$', automate.del_project, name='projectdel'),
    url(r'^setting/module/add/$', automate.add_module, name='moduleadd'),
    url(r'^setting/module/list/$', login_required(automate.ModuleListIndex.as_view()), name='modulelist'),
    url(r'^setting/module/update/$', automate.update_module, name='moduleupdate'),
    url(r'^setting/module/del/(?P<id>\d+)/$', automate.del_module, name='moduledel'),
    url(r'^setting/get/project/$', automate.get_project, name='getproject'),
    url(r'^setting/get/module/$', automate.get_module, name='getmodule'),
    url(r'^setting/get/connecteduser/$', automate.get_connected_user, name='getconnecteduser'),
    url(r'^setting/product/user/$', automate.product_user, name='productuser'),
    url(r'^setting/get/moduleList/$', automate.get_module_list, name='getmodulelist'),
    url(r'^setting/setedit/product/$', automate.set_edit_product, name='seteditproduct'),
    url(r'^setting/setedit/project/$', automate.set_edit_project, name='seteditproject'),
    url(r'^setting/setedit/module/$', automate.set_edit_module, name='seteditmodule'),
    url(r'^setting/setedit/user/$', automate.set_edit_user, name='setedituser'),
    url(r'^interf/web/home/$',  login_required(interface.WebinterfaceListIndex.as_view()), name='webinterface'),
    url(r'^interf/get/response/$', interface.get_response, name='getresponse'),
    url(r'^tools/syslog/home/$', automate.page_syslog, name='toolsyslog'),
    url(r'^tools/snmp/home/$', automate.comingsoon, name='toolsnmp'),
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^user/login', devicemgt.user_login),
    # url(r'^device/usedList', devicemgt.device_used_detail_info),
    # url(r'^device/list', devicemgt.device_table_info, name='device_detail'),
    # url(r'^device/borrow', devicemgt.bowrrow_device, name='borrow_device'),
    # url(r'^device/sendBack', devicemgt.sendback_device, name='device_sendBack'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


