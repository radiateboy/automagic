from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth import views as contrib_auth_views
from django.contrib.auth.decorators import login_required
from automatic.testcase import views

urlpatterns = [
    url(r'^add/$', views.add_case, name='caseadd'),
    url(r'^list/$|^$|^index/$', login_required(views.CaseListIndex.as_view()), name='caselist'),
    url(r'^view/(?P<id>\d+)/$', views.view_case, name='caseview'),
    url(r'^update/(?P<id>\d+)/$', views.update_case, name='caseupdate'),
    url(r'^copy/(?P<id>\d+)/$', views.copy_case, name='copycase'),
    url(r'^del/(?P<id>\d+)/$', views.del_case, name='casedel'),
    url(r'^run/$', views.run_case, name='runcase'),
    url(r'^caselist/$', views.get_caselist, name='getcase'),
    url(r'^step/del/(?P<id>\d+)/$', views.del_step, name='stepdel'),
]