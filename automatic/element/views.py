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
from automatic.management.models import Project, UserAndProduct
from automatic.element.models import Element

# Create your views here.


class ElementListIndex(ListView):
    context_object_name = 'elementlist'
    template_name = 'element/element.html'
    paginate_by = 10
    elementsum = 0
    model = Element
    http_method_names = [u'get']

    def get_queryset(self):
        prodcutid = UserAndProduct.objects.filter(username=self.request.user).values('productname')
        elementlist = Element.objects.filter(projectid__in=Project.objects.filter(productid__in=prodcutid).values('id')).order_by('-pk')
        prodcutid = self.request.GET.get('check_productname')
        projectid = self.request.GET.get('projectid')
        moduleid = self.request.GET.get('moduleid')
        keyword = self.request.GET.get('keyword')
        if prodcutid and int(prodcutid):
            elementlist = elementlist.filter(projectid__in=Project.objects.filter(productid=prodcutid).values('id'))
        if projectid:
            elementlist = elementlist.filter(projectid=projectid)
        if moduleid:
            elementlist = elementlist.filter(moduleid=moduleid)
        if keyword:
            elementlist = elementlist.filter(Q(id__icontains=keyword)|Q(location__icontains=keyword)|Q(descr__icontains=keyword))
        self.elementsum = len(elementlist)
        return  elementlist

    def get_context_data(self, **kwargs):
        context = super(ElementListIndex,self).get_context_data(**kwargs)
        namelist = Element.objects.values('descr').annotate()
        context['descr'] = namelist
        context['elementsum'] = self.elementsum
        context['elementform'] = FormElement()
        context['userandproduct'] = UserAndProduct.objects.all()
        return context

@csrf_exempt
@login_required()
def add_element(request):
    if request.method == 'POST':
        descr = request.POST['descr']
        projectid = request.POST['projectid']
        moduleid = request.POST['moduleid']
        locmode = request.POST['locmode']
        location = request.POST['location']
        createat = request.user.username
        updateat = request.user.username
        mid = Module.objects.get(pk=int(moduleid))
        pid = Project.objects.get(pk=int(projectid))
        ele = Element(moduleid=mid, projectid=pid, descr=descr, locmode=locmode, location=location, createat=createat, updateat=updateat)
        ele.save()
        # return HttpResponse(descr + '@' + locmode + '@' + location + '@' + str(mid.pk))
        return HttpResponse('添加元素成功。')
    else:
        return HttpResponse('添加元素失败。')


@csrf_exempt
@login_required()
def update_element(request):
    if request.method == 'POST':
        post_dict = request.POST
        element_dict = {"id":post_dict['elementid'],
                        "descr": post_dict['eledescr'],
                        "projectid":post_dict['ele_add_projectid'],
                        "moduleid": post_dict['moduleid'],
                        "locmode": post_dict['locmode'],
                        "location": post_dict['elelocation'],
                        }
        id = element_dict.get('id')
        descr = element_dict.get('descr')
        projectid = element_dict.get('projectid')
        moduleid = element_dict.get('moduleid')
        locmode = element_dict.get('locmode')
        location = element_dict.get('location')
        updateat = request.user.username
        updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        e = Element.objects.filter(id=int(id))
        e.update(descr=descr, projectid=projectid,moduleid=moduleid,locmode=locmode, location=location,updateat=updateat,updatetime=updatetime)
        return HttpResponse('修改成功')
    else:
        return HttpResponse('修改失败')


@login_required()
def del_element(request, id):
    element = get_object_or_404(Element, pk=int(id))
    element.delete()
    return HttpResponseRedirect(reverse('elementlist'))


@login_required()
def get_element(request):
    elementlist = []
    projectid = request.GET['projectid']
    elelista = Element.objects.raw("select id,(select name from management_module where id= moduleid_id) as modulename,locmode,location,descr from element_element where projectid_id="+projectid)
    for i in elelista:
        element = {}
        element['moduleid'] = i.modulename
        element['key'] = i.id
        location = i.locmode + "," + i.location
        element['location'] = location
        element['value'] = "["+str(i.id)+"][" + i.modulename + "]" + i.descr
        elementlist.append(element)
    return HttpResponse(json.dumps(elementlist))


@login_required()
def set_edit_element(request):
    elementid = request.GET['elementid']
    element = Element.objects.get(pk=elementid)
    elementinfo = {}
    elementinfo['id'] = element.pk
    elementinfo['descr'] = element.descr
    elementinfo['projectid'] = element.projectid.pk
    elementinfo['moduleid'] = element.moduleid.pk
    elementinfo['locmode'] = element.locmode
    elementinfo['location'] = element.location
    elementlist = [elementinfo]
    return HttpResponse(json.dumps(elementlist))
