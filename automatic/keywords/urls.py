from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from automatic.keywords import views

urlpatterns = [
    url(r'list/$', login_required(views.KeyWordListIndex.as_view()), name='keywordlist'),
    url(r'add/$', views.add_keyword, name='keywordadd'),
    url(r'update/$', views.update_keyword, name='keywordupdate'),
    url(r'del/(?P<id>\d+)/$', views.del_keyword, name='keyworddel'),
    url(r'get/$', views.get_keyword, name='getkeyword'),
    url(r'setedit/$', views.set_edit_keyword, name='seteditelement'),
]