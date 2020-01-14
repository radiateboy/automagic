from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from automatic.element import views

urlpatterns = [
    url(r'list/$', login_required(views.ElementListIndex.as_view()), name='elementlist'),
    url(r'add/$', views.add_element, name='elementadd'),
    url(r'update/$', views.update_element, name='elementupdate'),
    url(r'del/(?P<id>\d+)/$', views.del_element, name='elementdel'),
    url(r'get/$', views.get_element, name='getelement'),
    url(r'setedit/$', views.set_edit_element, name='seteditelement'),
]