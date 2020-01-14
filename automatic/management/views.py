# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2020-01-06
"""
import logging,json,os,time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.db.models import Q
from django.urls import reverse

from automatic.management.models import Product, Project, Module, User, UserAndProduct
from automatic.testcase.models import Case
# Create your views here.
@login_required()
def add_product(request):
    if request.method == 'POST':
        post_dict = request.POST
        product_dict = {"name": post_dict['productname'],
                        "descr": post_dict['descr'],
                        "sortby":post_dict['sortby'],
                        # "isenabled": post_dict['isenabled'],
                        }
        if 'isenabled' in post_dict:
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
        if 'isenabled' in post_dict:
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
        return render(request, 'management/productview.html', {'product':product,'projectlist':projectlist})
    else:
        errors.append('Error!!!')
        return render(request, 'management/productlist.html', {'errors', errors})
#
# def productlist(request):
#    productlist = Product.objects.all()
#    return render_to_response('productlist.html', {'productlist': productlist})


class ProductListIndex(ListView):
    context_object_name = 'productlist'
    template_name = 'management/productlist.html'
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
    template_name = 'management/projectlist.html'
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
        if 'isenabled' in post_dict:
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
        if 'isenabled' in post_dict:
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
        product = project.productid
        modulelist = project.module_set.all().order_by('-sortby')
        return render(request, 'management/projectview.html', {'project':project,'product':product,'modulelist':modulelist})
    else:
        errors.append('Error!!!')
        return render(request, 'management/projectview.html', {'errors', errors})


class ModuleListIndex(ListView):
    context_object_name = 'modulelist'
    template_name = 'management/modulelist.html'
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

@csrf_exempt
@login_required()
def add_module(request):
    if request.method == 'POST':
        post_dict = request.POST
        project_dict = {"projectid":post_dict['projectid'],
                        "name": post_dict['modulename'],
                        "sortby":post_dict['sortby'],
                        }
        if 'isenabled' in post_dict:
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
        if 'isenabled' in post_dict:
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
def del_module(request, id):
    module = get_object_or_404(Module,pk=int(id))
    module.delete()
    return HttpResponseRedirect('/setting/project/view/'+str(module.projectid_id))


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
    userandproduct = UserAndProduct.objects.filter(productname=productid)
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



@csrf_exempt
@login_required()
def product_user(request):
    if request.method == 'POST':
        post_dict = request.POST
        username = post_dict.getlist('realname')
        productname = post_dict['product']
        UserAndProduct.objects.filter(productname=productname).delete()
        for i in range(0, len(username)):
            userandproduct = UserAndProduct(username=User.objects.get(pk=username[i]),productname=Product.objects.get(pk=productname))
            userandproduct.save()
        return HttpResponse('授权成功')
    else:
        return HttpResponse('授权失败')


def page_syslog(request):
    return render(request, 'management/syslog.html')


def comingsoon(request):
    return render(request, 'comingsoon.html')
