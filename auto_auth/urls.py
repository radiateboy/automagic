# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth import views as contrib_auth_views
from django.contrib.auth.decorators import login_required
from auto_auth import views

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/profile/$', views.profile,
        name='auto-profile'),

    url(r'^register/$', views.register, name='auto-register'),

    url(r'^confirm/(?P<activation_key>[A-Za-z0-9\-]+)/$', views.confirm,
        name='auto-confirm'),

    url(r'^user/add/$', views.add_user, name='adduser'),
    url(r'^user/list/$', login_required(views.UserListIndex.as_view()), name='userlist'),
    url(r'^user/update/$', views.update_user, name='userupdate'),
    url(r'^user/del/(?P<id>\d+)/$', views.del_user, name='userdel'),
    url(r'^setedit/user/$', views.set_edit_user, name='setedituser'),

    url(r'^login/$', views.LoginViewWithCustomTemplate.as_view(), name='auto-login'),
    url(r'^logout/$',
        contrib_auth_views.LogoutView.as_view(next_page=reverse_lazy('auto-login')),
        name='auto-logout'),

    url(r'^passwordreset/$', contrib_auth_views.PasswordResetView.as_view(),
        name='auto-password_reset'),
    url(r'^passwordreset/done/$', contrib_auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    url(r'^passwordreset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        contrib_auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^passwordreset/complete/$',
        contrib_auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
