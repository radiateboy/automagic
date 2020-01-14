from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from automatic.testtask import views

urlpatterns = [
    url(r'add/$', views.add_task, name='taskadd'),
    url(r'list/$', login_required(views.TaskListIndex.as_view()), name='tasklist'),
    url(r'settreetask/$', views.set_tree_task, name='settreetask'),
    url(r'update/(?P<id>\d+)/$', views.update_task, name='taskupdate'),
    url(r'del/(?P<id>\d+)/$', views.del_task, name='taskdel'),
    url(r'run/$', views.run_task, name='runtask'),
    url(r'taskhistory/$', views.get_task_history, name='gettaskhistroy'),
]