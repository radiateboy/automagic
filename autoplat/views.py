# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2016-08-03
"""
import logging,json,os,time,jenkins

import subprocess
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from autoplat.forms import *
from django.views.generic import ListView
from autoplat.models import *
from django.db.models import Q
from django.core.urlresolvers import reverse

from rest_framework import viewsets
from autoplat.serializers import *
# Create your views here.

logger = logging.getLogger(__name__)

@login_required()
def index(request):
    user = request.user
    if user.is_admin:
        pdlist = UserandProduct.objects.all()
    else:
        pdlist = UserandProduct.objects.filter(username=user)
    # pjlist = Project.objects.all()
    return render(request, 'index1.html')

def comingsoon(request):
    return render(request, 'comingsoon.html')

def nav(request):
    List = map(str, range(10))
    List = {'name':'tsbc520', 'mail':'tsbc@vip.qq.com'}
    return  render(request, 'nav.html',{'List':List})


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
    return render(request, "login.html")


def _logout(request):
    logout(request)
    return redirect("/login")

@login_required()
def add_product(request):
    if request.method == 'POST':
        post_dict = request.POST
        product_dict = {"name": post_dict['productname'],
                        "descr": post_dict['descr'],
                        "sortby":post_dict['sortby'],
                        # "isenabled": post_dict['isenabled'],
                        }
        if post_dict.has_key('isenabled'):
            isenabled = True
        else:
            isenabled = False
        name = product_dict.get('name')
        isenabled = isenabled
        descr = product_dict.get('descr')
        sortby = product_dict.get('sortby')
        createat = request.user.username
        updateat = request.user.username
        product = Product(name=name, isenabled=isenabled,descr=descr,sortby=sortby, createat=createat, updateat=updateat)
        product.save()
        return HttpResponse('创建成功')
    else:
        return HttpResponse('创建失败')

@csrf_exempt
@login_required()
def update_product(request):
    if request.method == 'POST':
        post_dict = request.POST
        product_dict = {"id":post_dict['productid'],
                        "name": post_dict['productname'],
                        "descr": post_dict['descr'],
                        "sortby":post_dict['sortby'],
                        # "isenabled": post_dict['isenabled'],
                        }
        if post_dict.has_key('isenabled'):
            isenabled = True
        else:
            isenabled = False
        id = product_dict.get('id')
        name = product_dict.get('name')
        isenabled = isenabled
        descr = product_dict.get('descr')
        sortby = product_dict.get('sortby')
        updateat = request.user.username
        updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        p = Product.objects.filter(id=int(id))
        p.update(name=name, isenabled=isenabled,descr=descr,sortby=sortby, updateat=updateat, updatetime=updatetime)
        return HttpResponse('修改成功')
    else:
        return HttpResponse('修改失败')

@login_required()
def del_product(request,id):
    product = get_object_or_404(Product,pk=int(id))
    product.delete()
    return HttpResponseRedirect(reverse('productlist'))

@csrf_exempt
@login_required()
def view_product(request, id):
    product = get_object_or_404(Product, pk=int(id))
    errors = []
    if int(id):
        product = Product.objects.get(pk=int(id))
        projectlist = product.project_set.all()
        return render(request, 'productview.html', {'product':product,'projectlist':projectlist})
    else:
        errors.append('Error!!!')
        return render(request, 'productlist.html', {'errors', errors})
#
# def productlist(request):
#    productlist = Product.objects.all()
#    return render_to_response('productlist.html', {'productlist': productlist})

class ProductListIndex(ListView):
    context_object_name = 'productlist'
    template_name = 'productlist.html'
    paginate_by = 10
    productsum = 0
    model = Product
    http_method_names = [u'get',]

    def get_queryset(self):
        productlist = Product.objects.all().order_by('-sortby')
        productname = self.request.GET.get('productname')
        keyword = self.request.GET.get('keyword')

        if productname:
            productlist = productlist.filter(name=productname)
        if keyword:
            productlist = productlist.filter(Q(name__icontains=keyword)|Q(descr__icontains=keyword))
        self.productsum = len(productlist)
        return  productlist

    def get_context_data(self, **kwargs):
        context = super(ProductListIndex,self).get_context_data(**kwargs)
        namelist = Product.objects.values('name').annotate()
        context['name'] = namelist
        context['productsum'] = self.productsum
        return context


class ProjectListIndex(ListView):
    context_object_name = 'projectlist'
    template_name = 'projectlist.html'
    paginate_by = 10
    projectsum = 0
    model = Project
    http_method_names = [u'get',]

    def get_queryset(self):
        projectlist = Project.objects.all().order_by('-sortby')
        productid = self.request.GET.get('productid')
        projectid = self.request.GET.get('projectid')
        keyword = self.request.GET.get('keyword')
        if productid:
            projectlist = projectlist.filter(productid=productid)
        if projectid:
            projectlist = projectlist.filter(id=projectid)
        if keyword:
            projectlist = projectlist.filter(Q(name__icontains=keyword)|Q(descr__icontains=keyword))
        self.projectsum = len(projectlist)
        return  projectlist

    def get_context_data(self, **kwargs):
        context = super(ProjectListIndex,self).get_context_data(**kwargs)
        namelist = Project.objects.values('name').annotate()
        context['name'] = namelist
        context['productlist'] = Product.objects.all().order_by('-sortby')
        context['productsum'] = self.projectsum
        return context

class ModuleListIndex(ListView):
    context_object_name = 'modulelist'
    template_name = 'modulelist.html'
    paginate_by = 10
    model = Module
    modulesum = 0
    http_method_names = [u'get']

    def get_queryset(self):
        modulelist = Module.objects.all().order_by('-sortby')
        projectid = self.request.GET.get('projectid')
        modulename = self.request.GET.get('modulename')
        keyword = self.request.GET.get('keyword')
        if projectid:
            modulelist = modulelist.filter(projectid=Project.objects.get(name=projectid).id)
        if modulename:
            modulelist = modulelist.filter(name=modulename)
        if keyword:
            modulelist = modulelist.filter(Q(name__icontains=keyword)|Q(descr__icontains=keyword))
        self.modulesum = len(modulelist)
        return  modulelist

    def get_context_data(self, **kwargs):
        context = super(ModuleListIndex,self).get_context_data(**kwargs)
        namelist = Module.objects.values('name').annotate()
        context['name'] = namelist
        context['modulesum'] = self.modulesum
        return context

class CaseListIndex(ListView):
    context_object_name = 'caselist'
    template_name = 'index.html'
    paginate_by = 10
    # raw_sql = "select * from autoplat_case where projectid_id in (select id from autoplat_project where productid_id in (select productname_id from autoplat_userandproduct where username_id=3));"
    casesum = 0
    model = Case
    http_method_names = [u'get']

    def get_queryset(self):
        prodcutid = UserandProduct.objects.filter(username = self.request.user).values('productname')
        caselist = Case.objects.filter(projectid__in=Project.objects.filter(productid__in=prodcutid).values('id')).order_by('-pk')
        prodcutid = self.request.GET.get('check_productname')
        projectid = self.request.GET.get('projectid')
        moduleid = self.request.GET.get('moduleid')
        casestatus = self.request.GET.get('casestatus')
        issmoke = self.request.GET.get('issmoke')
        keyword = self.request.GET.get('keyword')
        if prodcutid and int(prodcutid):
            caselist = caselist.filter(projectid__in=Project.objects.filter(productid=prodcutid).values('id'))
        if projectid:
            caselist = caselist.filter(projectid=projectid)
        if moduleid:
            caselist = caselist.filter(moduleid=moduleid)
        if casestatus:
            caselist = caselist.filter(isenabled=casestatus)
        if issmoke:
            caselist = caselist.filter(issmoke=issmoke)
        if keyword:
            caselist = caselist.filter(Q(pk__icontains=keyword)|Q(casedesc__icontains=keyword)|Q(createat__icontains=keyword))
        self.casesum = len(caselist)
        return  caselist

    def get_context_data(self, **kwargs):
        context = super(CaseListIndex,self).get_context_data(**kwargs)
        # namelist = Case.objects.values('casedesc').annotate()
        # context['casedesc'] = namelist
        context['projectlist'] = Project.objects.all().order_by('-sortby')
        context['modulelist'] = Module.objects.all().order_by('-sortby')
        # context['productlist'] = Product.objects.all().order_by('-sortby')
        context['userandproduct'] = UserandProduct.objects.all()
        context['casesum'] = self.casesum
        return context

class ElementListIndex(ListView):
    context_object_name = 'elementlist'
    template_name = 'element.html'
    paginate_by = 10
    elementsum = 0
    model = Element
    http_method_names = [u'get']

    def get_queryset(self):
        prodcutid = UserandProduct.objects.filter(username=self.request.user).values('productname')
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
        context['userandproduct'] = UserandProduct.objects.all()
        return context

class KeyWordListIndex(ListView):
    context_object_name = 'keywordlist'
    template_name = 'keyword.html'
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
        context['userandproduct'] = UserandProduct.objects.all()
        context['productlist'] = Product.objects.all()
        context['keywordsum'] = self.keywordsum
        return context

@csrf_exempt
@login_required()
def add_project(request):
    if request.method == 'POST':
        post_dict = request.POST
        project_dict = {"productid":post_dict['productid'],
                        "name": post_dict['projectname'],
                        "descr": post_dict['descr'],
                        "sortby":post_dict['sortby'],
                        "version": post_dict['version'],
                        }
        if post_dict.has_key('isenabled'):
            isenabled = True
        else:
            isenabled = False
        productid = project_dict.get('productid')
        name = project_dict.get('name')
        isenabled = isenabled
        descr = project_dict.get('descr')
        version = project_dict.get('version')
        sortby = project_dict.get('sortby')
        createat = request.user.username
        updateat = request.user.username

        project = Project(productid=Product.objects.get(pk=productid), name=name, isenabled=isenabled, version=version, descr=descr,sortby=sortby,
                              createat=createat, updateat=updateat)
        project.save()

        return HttpResponse('创建成功')
    else:
        return HttpResponse('创建失败')


@csrf_exempt
@login_required()
def update_project(request):
    if request.method == 'POST':
        post_dict = request.POST
        project_dict = {"id":post_dict['projectid'],
                        "name": post_dict['projectname'],
                        "descr": post_dict['descr'],
                        "version":post_dict['version'],
                        "sortby":post_dict['sortby'],
                        # "isenabled": post_dict['isenabled'],
                        }
        if post_dict.has_key('isenabled'):
            isenabled = True
        else:
            isenabled = False
        id = project_dict.get('id')
        name = project_dict.get('name')
        isenabled = isenabled
        descr = project_dict.get('descr')
        version = project_dict.get('version')
        sortby = project_dict.get('sortby')
        updateat = request.user.username
        updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        p = Project.objects.filter(id=int(id))
        p.update(name=name, isenabled=isenabled,descr=descr, version=version ,sortby=sortby, updateat=updateat, updatetime=updatetime)
        return HttpResponse('修改成功')
    else:
        return HttpResponse('修改失败')

@login_required()
def del_project(request,id):
    project = get_object_or_404(Project,pk=int(id))
    x = project.productid
    project.delete()
    return HttpResponseRedirect('/setting/product/view/' + str(Product.objects.get(name=x).id))


@csrf_exempt
@login_required()
def view_project(request, id):
    project = get_object_or_404(Project, pk=int(id))
    errors = []
    if int(id):
        product = Product.objects.get(name=project.productid)
        modulelist = project.module_set.all().order_by('-sortby')
        return render(request, 'projectview.html', {'project':project,'product':product,'modulelist':modulelist})
    else:
        errors.append('Error!!!')
        return render(request, 'projectview.html', {'errors', errors})


@csrf_exempt
@login_required()
def add_module(request):
    if request.method == 'POST':
        post_dict = request.POST
        project_dict = {"projectid":post_dict['projectid'],
                        "name": post_dict['modulename'],
                        "sortby":post_dict['sortby'],
                        }
        if post_dict.has_key('isenabled'):
            isenabled = True
        else:
            isenabled = False
        projectid = project_dict.get('projectid')
        name = project_dict.get('name')
        isenabled = isenabled
        sortby = project_dict.get('sortby')
        createat = request.user.username
        updateat = request.user.username

        module = Module(projectid=Project.objects.get(pk=projectid), name=name, isenabled=isenabled, sortby=sortby,
                              createat=createat, updateat=updateat)
        module.save()

        return HttpResponse('创建成功')
    else:
        return HttpResponse('创建失败')

@csrf_exempt
@login_required()
def update_module(request):
    if request.method == 'POST':
        post_dict = request.POST
        module_dict = {"id":post_dict['moduleid'],
                        "name": post_dict['modulename'],
                        "sortby":post_dict['sortby'],
                        # "isenabled": post_dict['isenabled'],
                        }
        if post_dict.has_key('isenabled'):
            isenabled = True
        else:
            isenabled = False
        id = module_dict.get('id')
        name = module_dict.get('name')
        isenabled = isenabled
        sortby = module_dict.get('sortby')
        updateat = request.user.username
        updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        m = Module.objects.filter(id=int(id))
        m.update(name=name, isenabled=isenabled,sortby=sortby, updateat=updateat, updatetime=updatetime)
        return HttpResponse('修改成功')
    else:
        return HttpResponse('修改失败')

@login_required()
def del_module(request,id):
    module = get_object_or_404(Module,pk=int(id))
    module.delete()
    return HttpResponseRedirect('/setting/project/view/'+str(Project.objects.get(name=module.projectid).id))

@login_required()
def add_case(request):
    if request.method == 'POST':
        post_dict = request.POST
        case_dict = {"projectid": post_dict['projectid'],
                     "moduleid": post_dict['moduleid'],
                     "casedesc": post_dict['casedesc'],
                     "testrailcaseid": post_dict['testrailcaseid'],
                     "dependent": post_dict['dependent']
                     }

        projectid = Project.objects.get(pk=int(case_dict.get('projectid')))
        moduleid = Module.objects.get(pk=int(case_dict.get('moduleid')))
        casedesc = case_dict.get('casedesc')
        if post_dict.has_key('isenabled'):
            isenabled = True
        else:
            isenabled = False
        if post_dict.has_key('issmoke'):
            issmoke = True
        else:
            issmoke = False
        testrailcaseid = case_dict.get('testrailcaseid')
        dependent = case_dict.get('dependent')
        createat = request.user.username
        updateat = request.user.username

        case = Case(projectid=projectid, moduleid=moduleid, casedesc=casedesc, isenabled=isenabled, createat=createat,
                    updateat=updateat, dependent=dependent,testrailcaseid=testrailcaseid,issmoke=issmoke)
        case.save()
        element_list = post_dict.getlist("elementid")
        keyword_list = post_dict.getlist("keyword")
        value_list, desc_list = post_dict.getlist("inputtext"), post_dict.getlist("descr")
        for keyword, element, inputtext, descr in zip(keyword_list, element_list, value_list, desc_list):
            kw = Keyword.objects.get(pk=int(keyword))
            if element != 'None':
                # print "aaaa", type(element)
                ele = Element.objects.get(pk=int(element))
                case.step_set.create(stepid=keyword, descr=descr, keywordid=kw, elementid=ele, inputtext=inputtext)
            else:
                # print "bbbb",element
                case.step_set.create(stepid=keyword, descr=descr, keywordid=kw,inputtext=inputtext)
        return HttpResponse('添加成功')
    else:
        userandproduct = UserandProduct.objects.all()
        projectlist = Project.objects.all().order_by('-sortby')
        modulelist = Module.objects.all().order_by('-sortby')
        caseform = FormCase()
        stepform = FormStep()
        # keywordform = FormKeyword()
        # elementform =FormElement()
        # keywordlist = Keyword.objects.all()
        return render(request, 'caseadd.html',{'userandproduct':userandproduct,'projectlist':projectlist,'modulelist':modulelist,'caseform':caseform,'stepform':stepform})


@csrf_exempt
@login_required()
def update_case(request, id):
    tcase = Case.objects.get(id=int(id))
    steplist = Step.objects.filter(caseid=tcase.id)
    if request.method == 'POST':
        post_dict = request.POST
        case = Case.objects.filter(id=int(id))
        case_dict = {"projectid": post_dict['projectid'],
                     "moduleid": post_dict['moduleid'],
                     "casedesc": post_dict['casedesc'],
                     "dependent": post_dict['dependent'],
                     "testrailcaseid": post_dict['testrailcaseid']
                     }

        projectid = Project.objects.get(pk=int(case_dict.get('projectid')))
        moduleid = Module.objects.get(pk=int(case_dict.get('moduleid')))
        testrailcaseid = case_dict.get('testrailcaseid')
        casedesc = case_dict.get('casedesc')
        if post_dict.has_key('isenabled'):
            isenabled = True
        else:
            isenabled = False
        if post_dict.has_key('issmoke'):
            issmoke = True
        else:
            issmoke = False
        dependent = case_dict.get('dependent')
        updateat = request.user.username
        updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        case.update(projectid=projectid, moduleid=moduleid, casedesc=casedesc, isenabled=isenabled,
                    updateat=updateat, dependent=dependent,testrailcaseid=testrailcaseid,updatetime=updatetime,issmoke=issmoke)
        keyword_list, element_list = post_dict.getlist("keyword"), post_dict.getlist("elementid")
        value_list, desc_list = post_dict.getlist("inputtext"), post_dict.getlist("descr")
        tcase.step_set.all().delete()
        for keyword, element, inputtext, descr in zip(keyword_list, element_list, value_list, desc_list):
            kw = Keyword.objects.get(pk=int(keyword))
            #print element
            if element != 'None':
                # print "ccc",element
                elementid = Element.objects.get(pk=int(element))
                tcase.step_set.create(stepid=keyword, descr=descr, keywordid=kw, elementid=elementid, inputtext=inputtext)
            else:
                # print "ddd",element
                tcase.step_set.create(stepid=keyword, descr=descr, keywordid=kw, inputtext=inputtext)
        return HttpResponse('添加成功')
    else:
        modulelist = Module.objects.filter(projectid=tcase.projectid).order_by('-sortby')
        project = Project.objects.get(name=tcase.projectid)
        projectlist = Project.objects.filter(productid=project.productid)
        keywordlist = Keyword.objects.filter(Q(productid=0)|Q(productid=project.productid.pk))
        elementlist = Element.objects.filter(projectid=project.pk)
        return render(request, 'caseedit.html', {'project':project,'modulelist':modulelist,'elementlist':elementlist,'projectlist':projectlist,'keywordlist':keywordlist,'steplist':steplist,'tcase':tcase})

@csrf_exempt
@login_required()
def copy_case(request, id):
    tcase = Case.objects.get(id=int(id))
    steplist = Step.objects.filter(caseid=tcase.id)
    if request.method == 'POST':
        post_dict = request.POST
        case_dict = {"projectid": post_dict['projectid'],
                     "moduleid": post_dict['moduleid'],
                     "casedesc": post_dict['casedesc'],
                     "dependent": post_dict['dependent'],
                     "testrailcaseid": post_dict['testrailcaseid']
                     }

        projectid = Project.objects.get(pk=int(case_dict.get('projectid')))
        moduleid = Module.objects.get(pk=int(case_dict.get('moduleid')))
        testrailcaseid = case_dict.get('testrailcaseid')
        casedesc = case_dict.get('casedesc')
        if post_dict.has_key('isenabled'):
            isenabled = True
        else:
            isenabled = False
        if post_dict.has_key('issmoke'):
            issmoke = True
        else:
            issmoke = False
        dependent = case_dict.get('dependent')
        createat = request.user.username
        updateat = request.user.username

        case = Case(projectid=projectid, moduleid=moduleid, casedesc=casedesc, isenabled=isenabled, createat=createat,
                        updateat=updateat, dependent=dependent, testrailcaseid=testrailcaseid, issmoke=issmoke)
        case.save()

        keyword_list, element_list = post_dict.getlist("keyword"), post_dict.getlist("elementid")
        value_list, desc_list = post_dict.getlist("inputtext"), post_dict.getlist("descr")
        for keyword, element, inputtext, descr in zip(keyword_list, element_list, value_list, desc_list):
            kw = Keyword.objects.get(pk=int(keyword))
            # print element
            if element != 'None':
                # print "ccc",element
                elementid = Element.objects.get(pk=int(element))
                case.step_set.create(stepid=keyword, descr=descr, keywordid=kw, elementid=elementid, inputtext=inputtext)
            else:
                # print "ddd",element
                case.step_set.create(stepid=keyword, descr=descr, keywordid=kw, inputtext=inputtext)
        return HttpResponse('添加成功')
    else:
        modulelist = Module.objects.filter(projectid=tcase.projectid).order_by('-sortby')
        project = Project.objects.get(name=tcase.projectid)
        projectlist = Project.objects.filter(productid=project.productid)
        keywordlist = Keyword.objects.filter(Q(productid=0) | Q(productid=project.productid.pk))
        elementlist = Element.objects.filter(moduleid=tcase.moduleid)
        return render(request, 'casecopy.html', {'project':project,'modulelist':modulelist,'elementlist':elementlist,'projectlist':projectlist,'keywordlist':keywordlist,'steplist':steplist,'tcase':tcase})


@login_required()
def del_case(request,id):
    case = get_object_or_404(Case,pk=int(id))
    case.delete()
    return HttpResponseRedirect(reverse('caselist'))


@login_required()
def del_step(request, id):
    step = get_object_or_404(Step, pk=int(id))
    caseid = step.caseid
    cid = Case.objects.get(casedesc=caseid)
    step.delete()
    return HttpResponseRedirect('/case/update/'+str(cid.pk))


@login_required()
def view_case(request, id):
    case = get_object_or_404(Case, pk=int(id))
    steplist = case.step_set.all()
    return render(request, 'caseview.html',locals())

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
        except Exception, e:
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
def get_project(request):
    projectlist = []
    productid = request.GET['productid']
    pjlist = Project.objects.filter(productid=productid)

    for i in pjlist:
        project = {}
        project['key'] = i.id
        project['value'] = i.name
        projectlist.append(project)
    return HttpResponse(json.dumps(projectlist))

@login_required()
def get_module(request):
    modulelist = []
    projectid = request.GET['projectid']
    if projectid == u'':
        return HttpResponse(u'[]')
    modlist = Module.objects.filter(projectid=projectid, isenabled=True)
    for i in modlist:
        module = {}
        module['key'] = i.id
        module['value'] = i.name
        modulelist.append(module)
    return HttpResponse(json.dumps(modulelist))

@login_required()
def get_connected_user(request):
    connecteduserlist=[]
    productid = request.GET['productid']
    #product = Product.objects.filter(pk=productid)[0].name
    userandproduct = UserandProduct.objects.filter(productname=productid)
    useridlist=userandproduct.values('username')
    for i in useridlist:
        user={}
        user['key'] = User.objects.get(pk=i['username']).pk
        user['username'] = User.objects.get(pk=i['username']).username
        user['realname'] = User.objects.get(pk=i['username']).realname
        connecteduserlist.append(user)
    return HttpResponse(json.dumps(connecteduserlist))

@login_required()
def get_module_list(request):
    post_dict = request.GET
    caselist = []
    projectid = post_dict['projectid']
    if post_dict['issmoke'] == '1':
        issmoke = True
    else:
        issmoke = False
    if projectid == u'':
        return HttpResponse(u'[]')
    if issmoke:
        cases = Case.objects.filter(projectid=projectid, issmoke=issmoke, isenabled=True).order_by("moduleid_id", "id")
    else:
        cases = Case.objects.filter(projectid=projectid, isenabled=True).order_by("moduleid_id", "id")

    moduleid = -1
    for case in cases:
        if moduleid != case.moduleid_id:
            moduleid = case.moduleid_id
            caselist.append(u'{id:9999999%s, pId:99999990, name:"%s"}' % (case.moduleid_id, case.moduleid.name))
        caselist.append(u'{id:%s, pId:9999999%s, name:"%s、%s"}' % (case.id, case.moduleid_id, case.id, case.casedesc))

    if caselist:
        caselist.insert(0, u'{id:99999990, pId:0, name:"%s", open:true}' % (case.projectid.name))
    caseData = u'[%s]' % u','.join(caselist)
    return HttpResponse(caseData)

@login_required()
def get_element(request):
    elementlist = []
    projectid = request.GET['projectid']
    elelista = Element.objects.raw("select id,(select name from autoplat_module where id= moduleid_id) as modulename,locmode,location,descr from autoplat_element where projectid_id="+projectid)
    for i in elelista:
        element = {}
        element['moduleid'] = i.modulename
        element['key'] = i.id
        location = i.locmode + "," + i.location
        element['location'] = location
        element['value'] = "["+str(i.id)+"][" + i.modulename+ "]" + i.descr
        elementlist.append(element)
    return HttpResponse(json.dumps(elementlist))

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
def set_edit_product(request):
    productid = request.GET['productid']
    product = Product.objects.get(pk=productid)
    pd = {}
    pd['id'] = product.pk
    pd['name'] = product.name
    pd['descr'] = product.descr
    pd['isenabled'] = product.isenabled
    pd['sortby'] = product.sortby
    productlist = [pd]
    return HttpResponse(json.dumps(productlist))

@login_required()
def set_edit_project(request):
    projectid = request.GET['projectid']
    project = Project.objects.get(pk=projectid)
    pj = {}
    pj['id'] = project.pk
    pj['name'] = project.name
    pj['descr'] = project.descr
    pj['isenabled'] = project.isenabled
    pj['version'] = project.version
    pj['sortby'] = project.sortby
    projectlist = [pj]
    return HttpResponse(json.dumps(projectlist))

@login_required()
def set_edit_module(request):
    moduleid = request.GET['moduleid']
    module = Module.objects.get(pk=moduleid)
    md = {}
    md['id'] = module.pk
    md['name'] = module.name
    md['isenabled'] = module.isenabled
    md['sortby'] = module.sortby
    modulelist = [md]
    return HttpResponse(json.dumps(modulelist))

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
    userinfo['testrailuser'] = user.testrailuser
    userinfo['testrailpass'] = user.testrailpass
    userlist = [userinfo]
    return HttpResponse(json.dumps(userlist))

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

@login_required()
def set_tree_task(request):
    taskid = request.GET['taskid']
    task = Task.objects.get(pk=taskid)
    # print elementinfo['projectid'],elementinfo['moduleid'],elementinfo['locmode']
    return HttpResponse(task.caselist)

def duration_change(num):
    if num == 0:
        x = 0
    else:
        x = str(num)[:-3]
    if int(x) <= 60:
        return str(x)+'s'
    elif int(x) < 3600:
        y = float(x)/60
        z = str(y).split('.')
        return z[0]+'min:'+ str(int(z[1])*6)[:2]+'s'
    else:
        y = divmod(int(x), 3600)
        z = float(y[1])/60
        m = str(z).split('.')
        return str(y[0])+'h:'+m[0]+'min:'+ str(int(m[1])*6)[:2]+'s'

def timeStamp(timastamp):
    timastamp = str(timastamp)[:10]
    timeArray = time.localtime(int(timastamp))
    chartime = time.strftime('%Y-%m-%d %H:%M:%S',timeArray)
    return chartime

def testreport(path):
    path = path[7:]
    return path

@csrf_exempt
@login_required()
def get_task_history(request):
    task_history = []
    taskid = request.GET['taskid']
    task = Task.objects.get(id=taskid)

    if task.tasktype == '1':
        taskhistory = Taskhistory.objects.filter(taskid=taskid).order_by('-id')[:20]
        for i in taskhistory:
            th = {}
            th['starttime'] = str(i.starttime)[:19]
            th['taskid'] = i.taskid.id
            th['tasktype'] = i.tasktype
            th['taskname'] = i.taskname
            th['case_tag_all'] = i.case_tag_all
            th['case_tag_pass'] = i.case_tag_pass
            th['case_tag_fail'] = i.case_tag_fail
            th['case_tag_error'] = i.case_tag_error
            if i.exectime is not None and len(i.exectime) > 7:
                th['exectime'] = i.exectime[:-7]
            th['user'] = i.userid.realname
            th['reporturl'] = i.reporturl
            task_history.append(th)
        return HttpResponse(json.dumps(task_history))
    elif task.tasktype == '2':
        taskhistory = Taskhistory.objects.filter(taskid=taskid).order_by('-id')
        for i in taskhistory:
            th = {}
            th['starttime'] = str(i.starttime)[:19]
            th['taskid'] = i.taskid.id
            th['tasktype'] = i.tasktype
            th['taskname'] = i.taskname
            th['reporturl'] = i.reporturl
            th['user'] = i.userid.realname
            task_history.append(th)
        return HttpResponse(json.dumps(task_history))
    elif task.tasktype == '3':
        jenkins_server_url = task.jenkins_server_url
        user_id = task.user_id
        api_token = task.api_token
        build_name = task.build_name
        url = 'http://jenkinsm.acorn-net.com/TestResults/'
        reportdir = '/'
        if task.projectid.productid.id == 1:
            reportdir = 'CornerStone/'
        elif task.projectid.productid.id in (4, 5):#根据productid在jenkins创建对应的result目录
            reportdir = 'GemStone/'
        url = url + reportdir
        try:
            server = jenkins.Jenkins(jenkins_server_url, user_id, api_token)
            jenkinsjob = server.get_job_info(task.build_name)
            for i in jenkinsjob['builds'][:40]:
                bi = server.get_build_info(build_name, i['number'])
                th={}
                th['starttime']= timeStamp(bi['timestamp'])
                th['build_name'] = bi['fullDisplayName']
                th['exectime'] = duration_change(bi['duration'])
                th['result'] = bi['result']
                th['user'] = bi['actions'][0]['causes'][0]['shortDescription']
                th['consoleurl'] = bi['url']+'console'
                if len(bi['artifacts'])>0:
                    th['reporturl'] = url+testreport(bi['artifacts'][0]['relativePath'])
                else:
                    th['reporturl'] = '#'
                task_history.append(th)
            return HttpResponse(json.dumps(task_history))
        except:
            return HttpResponse(json.dumps(task_history))

def get_caselist(request):
    caseid = request.GET['caseid']
    projectid = Case.objects.get(pk=caseid).projectid
    caselist = Case.objects.filter(projectid=projectid).order_by('id')
    casenum = []
    for i in caselist:
        caseno = {}
        caseno['caseid'] = i.pk
        casenum.append(i.pk)
        casenum.append(',')
    return HttpResponse(casenum)

def run_case(request):
    caseid = request.GET['caseid']
    depentid = Case.objects.get(pk=caseid).dependent
    if depentid == u'':
        os.system("python seleniumkeyword/TestSuite.py -c %d" % int(caseid))
    else:
        os.system("python seleniumkeyword/TestSuite.py -c " + depentid + "," + caseid)
    # print caseid
    return HttpResponse('true')


class TaskListIndex(ListView):
    context_object_name = 'tasklist'
    template_name = 'tasklist.html'
    paginate_by = 10
    # raw_sql = "select * from autoplat_case where projectid_id in (select id from autoplat_project where productid_id in (select productname_id from autoplat_userandproduct where username_id=3));"
    tasksum = 0
    queryset = Task.objects.filter(projectid=3)
    http_method_names = [u'get']

    def get_queryset(self):
        tasklist = Task.objects.all().order_by('-pk')
        prodcutid = UserandProduct.objects.filter(username=self.request.user).values('productname')
        tasklist = Task.objects.filter(projectid__in=Project.objects.filter(productid__in=prodcutid).values('id')).order_by('-pk')
        prodcutid = self.request.GET.get('check_productname')
        projectid = self.request.GET.get('projectid')
        tasktype = self.request.GET.get('tasktype')
        keyword = self.request.GET.get('keyword')

        if prodcutid and int(prodcutid):
            tasklist = tasklist.filter(projectid__in=Project.objects.filter(productid=prodcutid).values('id'))
        if projectid:
            tasklist = tasklist.filter(projectid=projectid)
        if tasktype:
            tasklist = tasklist.filter(tasktype=tasktype)
        else:
            tasklist = tasklist.filter(tasktype=1)
        if keyword:
            tasklist = tasklist.filter(Q(pk__icontains=keyword)|Q(taskname__icontains=keyword)|Q(createat__icontains=keyword))
        self.tasksum = len(tasklist)
        return  tasklist

    def get_context_data(self, **kwargs):
        context = super(TaskListIndex,self).get_context_data(**kwargs)
        # tasklist = Task.objects.values('taskname').annotate()
        context['tasksum'] = self.tasksum
        # context['productlist'] = Product.objects.all().order_by('-sortby')
        context['userandproduct'] = UserandProduct.objects.all()
        return context


@csrf_exempt
@login_required()
def add_task(request):
    if request.method == 'POST':
        post_dict = request.POST
        taskname = post_dict['taskname']
        runid = post_dict['testrailrunid']
        sectionid = post_dict['testsectionid']
        suitesid = post_dict['testrailsuites']
        api_token = post_dict['api_token']
        jenkins_server_url = post_dict['jenkins_server_url']
        user_id = post_dict['user_id']
        build_name = post_dict['build_name']
        projectid = Project.objects.get(pk=int(post_dict['projectid']))
        caseids = post_dict['caseids']
        tasktype = post_dict['tasktype']
        issmoke = post_dict['issmoke']
        if int(issmoke):
            issmoke = True
        else:
            issmoke = False
        createat = request.user.username
        updateat = request.user.username
        task = Task(taskname=taskname, testrailrunid=runid, testrailsuites=suitesid, testsectionid=sectionid, projectid=projectid,
                        api_token=api_token,jenkins_server_url=jenkins_server_url,caselist=caseids, tasktype=tasktype,
                    user_id=user_id,build_name=build_name,createat=createat, updateat=updateat, issmoke=issmoke)
        task.save()
        if post_dict.has_key('codename'):
            codename_list,codedescr_list, codevalue_list = post_dict.getlist("codename"),post_dict.getlist("codedescr"), post_dict.getlist("codevalue")
            for codename, codedescr, codevalue in zip(codename_list, codedescr_list, codevalue_list):
                    task.codelist_set.create(codedescr=codedescr, codename=codename, codevalue=codevalue)
        return HttpResponse('任务创建成功')
    else:
        userandproduct = UserandProduct.objects.all()
        projectlist = Project.objects.all().order_by('-sortby')
        modulelist = Module.objects.all().order_by('-sortby')
        caselist =  Case.objects.filter(isenabled=True)
        return render(request, 'taskadd.html',{'userandproduct':userandproduct,'projectlist':projectlist,'modulelist':modulelist,'caselist':caselist})

@csrf_exempt
@login_required()
def update_task(request,id):
    taskinfo = Task.objects.get(pk=id)
    project = Project.objects.get(pk=taskinfo.projectid.pk)
    print project
    if request.method == 'POST':
        post_dict = request.POST
        taskname = post_dict['taskname']
        testrailrunid = post_dict['testrailrunid']
        testsectionid = post_dict['testsectionid']
        suitesid = post_dict['testrailsuites']
        api_token = post_dict['api_token']
        jenkins_server_url = post_dict['jenkins_server_url']
        user_id = post_dict['user_id']
        build_name = post_dict['build_name']
        projectid = Project.objects.get(pk=int(post_dict['projectid']))
        caseids = post_dict['caseids']
        tasktype = post_dict['tasktype']
        issmoke = post_dict['issmoke']
        if int(issmoke):
            issmoke = True
        else:
            issmoke = False
        updateat = request.user.username
        updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        task = Task.objects.filter(pk= id)
        task.update(projectid=projectid, taskname=taskname, tasktype=tasktype, status = 0,caselist=caseids, testrailrunid=testrailrunid,
                    api_token=api_token,jenkins_server_url=jenkins_server_url,updateat=updateat, updatetime=updatetime,
                    user_id=user_id,build_name=build_name,testsectionid=testsectionid,testrailsuites=suitesid,issmoke=issmoke)
        taskinfo.codelist_set.all().delete()
        codename_list, codedescr_list, codevalue_list = post_dict.getlist("codename"), post_dict.getlist("codedescr"), post_dict.getlist("codevalue")
        for codename, codedescr, codevalue in zip(codename_list, codedescr_list, codevalue_list):
            taskinfo.codelist_set.create(codedescr=codedescr, codename=codename, codevalue=codevalue,updateat=updateat)
        return HttpResponse('任务修改成功')
    else:
        userandproduct = UserandProduct.objects.all()
        projectlist = Project.objects.filter(productid=project.productid).order_by('-sortby')
        modulelist = Module.objects.all().order_by('-sortby')
        caselist =  Case.objects.filter(isenabled=True)
        taskcase = taskinfo.caselist
        codelist = Codelist.objects.filter(taskid=id)
        casesum = len(taskcase.split(','))
        return render(request, 'taskedit.html',{'taskinfo':taskinfo,'codelist':codelist, 'casesum':casesum, 'userandproduct':userandproduct,'projectlist':projectlist,'modulelist':modulelist,'caselist':caselist})

def del_task(request,id):
    task = get_object_or_404(Task, pk=int(id))
    task.delete()
    return HttpResponseRedirect(reverse('tasklist'))

@csrf_exempt
@login_required()
def run_task(request):
    taskid = request.GET['taskid']
    userid = request.user.username
    task = Task.objects.get(pk=taskid)
    tasktype = task.tasktype
    runid = task.testrailrunid
    sectionid = task.testsectionid
    if tasktype == '1':
        if runid:
            os.system("python seleniumkeyword/TestSuite.py -t %s -u %s -r %s &" % (taskid, userid, runid))
        else:
            os.system("python seleniumkeyword/TestSuite.py -t %s &" % taskid )
    elif tasktype == '2':
        os.system("python seleniumkeyword/AddCase.py -t %s -u %s -s %s &" % (taskid, userid, sectionid))
        starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        task.status = 1
        task.save()
        caselist = task.caselist
        th = Taskhistory(taskid=task, userid=request.user, tasktype='2', taskname=task.taskname, starttime=starttime,reporturl=caselist)
        th.save()
    elif tasktype == '3':
        jenkins_server_url = task.jenkins_server_url
        user_id = task.user_id
        api_token = task.api_token
        build_name = task.build_name

        server = jenkins.Jenkins(jenkins_server_url,user_id,api_token)
        starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        server.build_job(build_name)
        task.status=1
        task.save()
        # build_num = jenkins.get_nextBuildNumber()
        # th = Taskhistory(taskid=task, userid=request.user, tasktype='3', taskname=task.taskname, starttime=starttime, build_name=task.build_name, build_number=build_num)
        # th.save()
    return HttpResponseRedirect(reverse('tasklist'))


class UserListIndex(ListView):
    context_object_name = 'userlist'
    template_name = 'userlist.html'
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
        return  userlist

    def get_context_data(self, **kwargs):
        context = super(UserListIndex,self).get_context_data(**kwargs)
        # userlist = User.objects.values('username').annotate()
        context['productlist'] = Product.objects.all().order_by('-sortby')
        context['userandproduct'] = UserandProduct.objects.all()
        context['usersum'] = self.usersum
        context['alluser']=self.alluser
        return context

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
                         "testrailuser": post_dict['testrailuser'],
                         "testrailpass": post_dict['testrailpass'],
                         }
        if post_dict.has_key('is_admin'):
            is_admin = True
        else:
            is_admin = False
        if post_dict.has_key('is_active'):
            is_active = True
        else:
            is_active = False
        username = user_dict.get('username')
        password = make_password(user_dict.get('password'),None,'pbkdf2_sha256')
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
                         "testrailuser": post_dict['testrailuser'],
                         "testrailpass": post_dict['testrailpass']
                         }
        if post_dict.has_key('is_admin'):
            is_admin = True
        else:
            is_admin = False
        if post_dict.has_key('is_active'):
            is_active = True
        else:
            is_active = False
        userid = user_dict.get('userid')
        username = user_dict.get('username')
        realname = user_dict.get('realname')
        email = user_dict.get('email')
        mobile = user_dict.get('mobile')
        dept = user_dict.get('dept')
        is_admin = is_admin
        is_active = is_active
        testrailuser = user_dict.get('testrailuser')
        testrailpass = user_dict.get('testrailpass')
        # updatetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        u = User.objects.filter(id=int(userid))
        # passwd = user_dict.get('password')
        if user_dict.get('password') == '':
            # print "AAA",username,user_dict.get('password')
            u.update(username=username, realname=realname, email=email,mobile=mobile,dept=dept,is_active=is_active,is_admin=is_admin,testrailuser=testrailuser,testrailpass=testrailpass)
        else:
            # print "BBB", username, user_dict.get('password')
            password = make_password(user_dict.get('password'), None, 'pbkdf2_sha256')
            u.update(username=username, password=password, realname=realname, dept=dept, email=email, mobile=mobile, is_active=is_active,
                        is_admin=is_admin, testrailuser=testrailuser, testrailpass=testrailpass)
        return HttpResponse('修改成功')
    else:
        return HttpResponse('修改失败')

def del_user(request,id):
    user = get_object_or_404(User, pk=int(id))
    user.delete()
    return HttpResponseRedirect(reverse('userlist'))

@csrf_exempt
@login_required()
def product_user(request):
    if request.method == 'POST':
        post_dict = request.POST
        username = post_dict.getlist('realname')
        productname = post_dict['product']
        UserandProduct.objects.filter(productname=productname).delete()
        for i in range(0, len(username)):
            userandproduct = UserandProduct(username=User.objects.get(pk=username[i]),productname=Product.objects.get(pk=productname))
            userandproduct.save()
        return HttpResponse('授权成功')
    else:
        return HttpResponse('授权失败')

def page_syslog(request):
    return render(request, 'syslog.html')


class ProductViewSet(viewsets.ModelViewSet):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer

class ProjectViewSet(viewsets.ModelViewSet):
        queryset = Project.objects.all()
        serializer_class = ProjectSerializer

class ModuleViewSet(viewsets.ModelViewSet):
        queryset = Module.objects.all()
        serializer_class = ModuleSerializer

class KeywordViewSet(viewsets.ModelViewSet):
        queryset = Keyword.objects.all()
        serializer_class = KeywordSerializer

class ElementViewSet(viewsets.ModelViewSet):
        queryset = Element.objects.all()
        serializer_class = ElementSerializer

class CaseViewSet(viewsets.ModelViewSet):
        queryset = Case.objects.all()
        serializer_class = CaseSerializer

class StepViewSet(viewsets.ModelViewSet):
        queryset = Step.objects.all()
        serializer_class = StepSerializer