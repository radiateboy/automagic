# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2020-01-08
"""
import time, json


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from automatic.element.forms import *
from django.views.generic import ListView
from automatic.element.models import *
from django.db.models import Q
from django.urls import reverse
from automatic.management.models import Product, Project, UserAndProduct
from automatic.keywords.models import Keyword


class KeyWordListIndex(ListView):
    context_object_name = 'keywordlist'
    template_name = 'keywords/keyword.html'
    paginate_by = 10
    keywordsum = 0
    model = Keyword
    http_method_names = [u'get']

    def get_queryset(self):
        keywordlist = Keyword.objects.all().order_by('-pk')
        keyword = self.request.GET.get('keyword')
        if keyword:
            keywordlist = keywordlist.filter(Q(keyword__icontains=keyword)|Q(kwdescr__icontains=keyword))
        self.keywordsum = len(keywordlist)
        return  keywordlist

    def get_context_data(self, **kwargs):
        context = super(KeyWordListIndex,self).get_context_data(**kwargs)
        context['userandproduct'] = UserAndProduct.objects.all()
        context['productlist'] = Product.objects.all()
        context['keywordsum'] = self.keywordsum
        return context


@login_required()
def add_keyword(request):
    if request.method == 'POST':
        name = request.POST['keyword']
        descr = request.POST['kwdescr']
        productid = request.POST['productid']
        createat = request.user.username
        updateat = request.user.username
        keyword = Keyword(productid=productid, keyword=name, kwdescr=descr, createat=createat, updateat=updateat)
        try:
            keyword.save()
        except Exception as e:
            return HttpResponse(e)
        return HttpResponse('添加关键字成功。')
    else:
        return HttpResponse('添加关键字失败。')


@csrf_exempt
@login_required()
def update_keyword(request):
    if request.method == 'POST':
        id = request.POST['keywordid']
        name = request.POST['keyword']
        descr = request.POST['kwdescr']
        productid = request.POST['productname']
        updateat = request.user.username
        updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        k = Keyword.objects.filter(id=int(id))
        k.update(productid=productid, keyword=name, kwdescr=descr, updateat=updateat, updatetime=updatetime)
        return HttpResponse('修改关键字成功。')
    else:
        return HttpResponse('修改关键字失败。')


@login_required()
def del_keyword(request, id):
    keyword = get_object_or_404(Keyword, pk=int(id))
    keyword.delete()
    return HttpResponseRedirect(reverse('keywordlist'))


@login_required()
def get_keyword(request):
    keywordlist = []
    productid = request.GET['productid']
    kwlist = Keyword.objects.filter(Q(productid=productid)|Q(productid=0))
    for i in kwlist:
        keywordinfo = {}
        keywordinfo['key'] = i.id
        keywordinfo['kwdescr'] = i.kwdescr
        keywordinfo['keyword'] = i.keyword
        keywordinfo['productid'] = i.productid
        keywordlist.append(keywordinfo)
    return HttpResponse(json.dumps(keywordlist))


@login_required()
def set_edit_keyword(request):
    keywordid = request.GET['keywordid']
    kw = Keyword.objects.get(pk=keywordid)
    keywordinfo = {}
    keywordinfo['id'] = kw.pk
    keywordinfo['descr'] = kw.kwdescr
    keywordinfo['name'] = kw.keyword
    keywordinfo['productid'] = kw.productid
    keywordlist = [keywordinfo]
    return HttpResponse(json.dumps(keywordlist))