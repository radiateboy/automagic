from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from automatic.management import views

urlpatterns = [
    url(r'^product/add/$', views.add_product, name='productadd'),
    url(r'^product/view/(?P<id>\d+)', views.view_product, name='productview'),
    url(r'^product/list/$', login_required(views.ProductListIndex.as_view()), name='productlist'),
    url(r'^product/update/$', views.update_product, name='productupdate'),
    url(r'^product/del/(?P<id>\d+)/$', views.del_product, name='productdel'),
    url(r'^project/add/$', views.add_project, name='projectadd'),
    url(r'^project/list/$', login_required(views.ProjectListIndex.as_view()), name='projectlist'),
    url(r'^project/view/(?P<id>\d+)', views.view_project, name='projectview'),
    url(r'^project/update/$', views.update_project, name='projectupdate'),
    url(r'^project/del/(?P<id>\d+)/$', views.del_project, name='projectdel'),
    url(r'^module/add/$', views.add_module, name='moduleadd'),
    # url(r'^module/list/$', login_required(views.ModuleListIndex.as_view()), name='modulelist'),
    url(r'^module/update/$', views.update_module, name='moduleupdate'),
    url(r'^module/del/(?P<id>\d+)/$', views.del_module, name='moduledel'),
    url(r'^get/project/$', views.get_project, name='getproject'),
    url(r'^get/module/$', views.get_module, name='getmodule'),
    url(r'^get/connecteduser/$', views.get_connected_user, name='getconnecteduser'),
    url(r'^product/user/$', views.product_user, name='productuser'),
    url(r'^get/moduleList/$', views.get_module_list, name='getmodulelist'),
    url(r'^setedit/product/$', views.set_edit_product, name='seteditproduct'),
    url(r'^setedit/project/$', views.set_edit_project, name='seteditproject'),
    url(r'^setedit/module/$', views.set_edit_module, name='seteditmodule'),
    url(r'^syslog/home/$', views.page_syslog, name='toolsyslog'),
    url(r'^snmp/home/$', views.comingsoon, name='toolsnmp'),
]