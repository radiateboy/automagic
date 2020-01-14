"""automatic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
from django.conf.urls import include, url
from auto_auth import urls as auth_urls
from automatic.testcase import urls as case_urls
from automatic.management import urls as mgt_urls
from automatic.element import urls as ele_urls
from automatic.keywords import urls as keywords_urls
from automatic.testtask import urls as task_urls
from automatic.webinterface import urls as interf_urls
from auto_auth.views import index

urlpatterns = [
    url('^$', index),
    url('^index/', index),
    url('admin/', admin.site.urls),
    url(r'^account/', include(auth_urls)),

    url(r'^setting/', include(mgt_urls)),

    url(r'^func/case/', include(case_urls)),

    url(r'^func/element/', include(ele_urls)),

    url(r'^func/keyword/', include(keywords_urls)),

    url(r'^func/task/', include(task_urls)),

    url(r'^interface/', include(interf_urls)),



    # url(r'^interf/web/home/$',  login_required(interface.WebinterfaceListIndex.as_view()), name='webinterface'),
    # url(r'^interf/get/response/$', interface.get_response, name='getresponse'),
    # url(r'^tools/syslog/home/$', automate.page_syslog, name='toolsyslog'),
    # url(r'^tools/snmp/home/$', automate.comingsoon, name='toolsnmp'),
    # url(r'^accounts/', include(oidc_urls)),
]
