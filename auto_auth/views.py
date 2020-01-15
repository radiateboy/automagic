# -*- coding: utf-8 -*-
import json

from datetime import datetime
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views
from django.views.decorators.http import require_GET
from django.utils.translation import ugettext_lazy as _
# from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.views.generic import ListView
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from auto_auth.models import User
from automatic.management.models import Product, UserAndProduct
from automatic.signals import USER_REGISTERED_SIGNAL
from auto_auth.forms import RegistrationForm
from auto_auth.models import UserActivationKey


class LoginViewWithCustomTemplate(views.LoginView):
    def get_template_names(self):
        return ['registration/custom_login.html', 'registration/login.html']


@login_required()
def index(request):
    return render(request, 'index.html')


def register(request):
    """Register method of account"""
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save()
            activation_key = form.set_activation_key()
            # send a signal that new user has been registered
            USER_REGISTERED_SIGNAL.send(sender=form.__class__,
                                        request=request,
                                        user=new_user)

            # Send confirmation email to new user
            if settings.DEFAULT_FROM_EMAIL and settings.AUTO_APPROVE_NEW_USERS:
                form.send_confirm_mail(request, activation_key)

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _('Your account has been created, please check your mailbox for confirmation')
                )
            else:
                messages.add_message(
                    request,
                    messages.WARNING,
                    _('Your account has been created, but you need an administrator to activate it')
                )
                messages.add_message(
                    request,
                    messages.INFO,
                    _('Following is the administrator list')
                )

                # super-users can approve others
                for user in User.objects.filter(is_superuser=True):
                    messages.add_message(
                        request,
                        messages.INFO,
                        '<a href="mailto:{}">{}</a>'.format(user.email,
                                                            user.get_full_name() or user.username)
                    )

                # site admins should be able to do so too
                for name, email in settings.ADMINS:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        '<a href="mailto:{}">{}</a>'.format(email, name)
                    )

            return HttpResponseRedirect(reverse('core-views-index'))
    else:
        form = RegistrationForm()

    context_data = {
        'form': form,
    }
    return render(request, 'registration/registration_form.html', context_data)


@require_GET
def confirm(request, activation_key):
    """Confirm the user registration"""

    # Get the object
    try:
        _activation_key = UserActivationKey.objects.select_related('user')
        _activation_key = _activation_key.get(activation_key=activation_key)
    except UserActivationKey.DoesNotExist:
        messages.add_message(
            request,
            messages.ERROR,
            _('This activation key no longer exists in the database')
        )
        return HttpResponseRedirect(request.GET.get('next', reverse('core-views-index')))

    if _activation_key.key_expires <= datetime.now():
        messages.add_message(request, messages.ERROR, _('This activation key has expired'))
        return HttpResponseRedirect(request.GET.get('next', reverse('core-views-index')))

    # All thing done, start to active the user and use the user login
    user = _activation_key.user
    user.is_active = True
    user.save(update_fields=['is_active'])
    _activation_key.delete()

    messages.add_message(
        request,
        messages.SUCCESS,
        _('Your account has been activated successfully')
    )
    return HttpResponseRedirect(request.GET.get('next', reverse('core-views-index')))


def profile(request, username):
    """Show user profiles"""
    user = get_object_or_404(User, username=username)
    return HttpResponseRedirect(reverse('admin:auth_user_change', args=[user.pk]))


def verify(request, query_dict):
    """验证用户名密码"""
    user = authenticate(username=query_dict["username"], password=query_dict["password"])
    if user is not None:
        login(request, user)
        return "verify_success"
    else:
        return u"用户名密码错误"


def login_page(request):
    if request.method == "POST":
        return HttpResponse(verify(request, request.POST))
    return render(request, "registration/login.html")


def _logout(request):
    logout(request)
    return redirect("/login")

@csrf_exempt
@login_required()
def add_user(request):
    if request.method == 'POST':
        post_dict = request.POST
        user_dict = {"username": post_dict['username'],
                     "realname": post_dict['realname'],
                     "password":post_dict['password'],
                     "email": post_dict['email'],
                     "mobile": post_dict['mobile'],
                     "dept": post_dict['dept'],
                     "testrailuser": post_dict['testrailuser'] if 'testrailuser' in post_dict else None,
                     "testrailpass": post_dict['testrailpass'] if 'testrailpass' in post_dict else None,
                     }
        if 'is_admin' in post_dict:
            is_admin = True
        else:
            is_admin = False
        if 'is_active' in post_dict:
            is_active = True
        else:
            is_active = False
        username = user_dict.get('username')
        password = make_password(user_dict.get('password'), None, 'pbkdf2_sha256')
        realname = user_dict.get('realname')
        email = user_dict.get('email')
        mobile = user_dict.get('mobile')
        dept = user_dict.get('dept')
        is_admin = is_admin
        is_active = is_active
        testrailuser = user_dict.get('testrailuser')
        testrailpass = user_dict.get('testrailpass')
        # print username,password,realname,email,mobile,is_admin,is_active,testrailuser,testrailpass
        try:
            User.objects.get(username=username).username
            return HttpResponse('用户名已经存在')
        except:
            pass
        try:
            User.objects.get(email=email).email
            return HttpResponse('邮箱地址已经被注册')
        except:
            pass
        user = User(username=username, password=password, realname=realname, email=email, mobile=mobile, dept=dept, is_active=is_active, is_admin=is_admin, testrailuser=testrailuser, testrailpass=testrailpass)
        user.save()
        return HttpResponse('创建成功')
    else:
        return HttpResponse('创建失败')


@csrf_exempt
@login_required()
def update_user(request):
    if request.method == 'POST':
        post_dict = request.POST
        user_dict = {"userid":post_dict['userid'],
                         "username": post_dict['username'],
                         "password": post_dict['password'],
                         "email":post_dict['email'],
                         "mobile": post_dict['mobile'],
                         "dept": post_dict['dept'],
                         "realname": post_dict['realname'],
                         "testrailuser": post_dict['testrailuser'] if 'testrailuser' in post_dict else None,
                         "testrailpass": post_dict['testrailpass'] if 'testrailpass' in post_dict else None,
                         }
        if 'is_admin' in post_dict:
            is_admin = True
        else:
            is_admin = False
        if 'is_active' in post_dict:
            is_active = True
        else:
            is_active = False
        userid = user_dict.get('userid')
        username = user_dict.get('username')
        realname = user_dict.get('realname')
        email = user_dict.get('email')
        mobile = user_dict.get('mobile')
        dept_str = user_dict.get('dept')
        dept = dept_str if dept_str else '测试'
        is_admin = is_admin
        is_active = is_active
        testrailuser = user_dict.get('testrailuser')
        testrailpass = user_dict.get('testrailpass')
        # updatetime = timezone.now()
        u = User.objects.filter(id=int(userid))
        # passwd = user_dict.get('password')
        if user_dict.get('password') == '':
            # print "AAA",username,user_dict.get('password')
            u.update(username=username, realname=realname, email=email,mobile=mobile, dept=dept,is_active=is_active,is_admin=is_admin,testrailuser=testrailuser,testrailpass=testrailpass)
        else:
            # print "BBB", username, user_dict.get('password')
            password = make_password(user_dict.get('password'), None, 'pbkdf2_sha256')
            u.update(username=username, password=password, realname=realname, dept=dept, email=email, mobile=mobile, is_active=is_active,
                        is_admin=is_admin, testrailuser=testrailuser, testrailpass=testrailpass)
        return HttpResponse('修改成功')
    else:
        return HttpResponse('修改失败')


@csrf_exempt
def del_user(request,id):
    user = get_object_or_404(User, pk=int(id))
    user.delete()
    return HttpResponseRedirect(reverse('userlist'))


@csrf_exempt
@login_required()
def set_edit_user(request):
    userid = request.GET['userid']
    user = User.objects.get(pk=userid)
    userinfo = {}
    userinfo['id'] = user.pk
    userinfo['username'] = user.username
    userinfo['password'] = user.password
    userinfo['email'] = user.email
    userinfo['mobile'] = user.mobile
    userinfo['is_admin'] = user.is_admin
    userinfo['is_active'] = user.is_active
    userinfo['realname'] = user.realname
    userinfo['dept'] = user.dept
    userinfo['testrailuser'] = user.testrailuser
    userinfo['testrailpass'] = user.testrailpass
    userlist = [userinfo]
    return HttpResponse(json.dumps(userlist))


class UserListIndex(ListView):
    context_object_name = 'userlist'
    template_name = 'oauth/userlist.html'
    paginate_by = 10
    model = User
    usersum = 0
    http_method_names = [u'get']
    alluser=[]

    def get_queryset(self):
        userlist = User.objects.all().order_by('-pk')
        self.alluser = User.objects.filter(is_active='True')
        keyword = self.request.GET.get('keyword')
        if keyword:
            userlist = userlist.filter(Q(username__icontains=keyword)|Q(email__icontains=keyword)|Q(mobile__icontains=keyword))
        self.usersum = len(userlist)
        return userlist

    def get_context_data(self, **kwargs):
        context = super(UserListIndex,self).get_context_data(**kwargs)
        # userlist = User.objects.values('username').annotate()
        context['productlist'] = Product.objects.all().order_by('-sortby')
        context['userandproduct'] = UserAndProduct.objects.all()
        context['usersum'] = self.usersum
        context['alluser']=self.alluser
        return context
