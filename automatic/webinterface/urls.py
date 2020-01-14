from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from automatic.webinterface import views

urlpatterns = [
    url(r'list/$',  login_required(views.WebinterfaceListIndex.as_view()), name='webinterface'),
    url(r'response/$', views.get_response, name='getresponse'),
]