# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2020-01-06
"""
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from automatic.testcase.forms import *
from django.views.generic import ListView
from automatic.management.models import Project, Module, UserAndProduct
from automatic.testcase.models import Case, Caseset
from automatic.keywords.models import Keyword
from automatic.element.models import Element
from django.db.models import Q
from django.urls import reverse

# Create your views here.


@login_required()
def add_case(request):
    if request.method == 'POST':
        post_dict = request.POST
        case_dict = {"projectid": post_dict['projectid'],
                     "moduleid": post_dict['moduleid'],
                     "casedesc": post_dict['casedesc'],
                     "testrailcaseid": post_dict['testrailcaseid'] if 'testrailcaseid' in post_dict else None,
                     "dependent": post_dict['dependent']
                     }

        projectid = Project.objects.get(pk=int(case_dict.get('projectid')))
        moduleid = Module.objects.get(pk=int(case_dict.get('moduleid')))
        casedesc = case_dict.get('casedesc')
        if 'isenabled' in post_dict:
            isenabled = True
        else:
            isenabled = False
        if 'issmoke' in post_dict:
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
        userandproduct = UserAndProduct.objects.all()
        projectlist = Project.objects.all().order_by('-sortby')
        modulelist = Module.objects.all().order_by('-sortby')
        caseform = FormCase()
        stepform = FormStep()
        # keywordform = FormKeyword()
        # elementform =FormElement()
        # keywordlist = Keyword.objects.all()
        return render(request, 'testcase/caseadd.html',{'userandproduct':userandproduct,'projectlist':projectlist,'modulelist':modulelist,'caseform':caseform,'stepform':stepform})


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
                     "testrailcaseid": post_dict['testrailcaseid'] if 'testrailcaseid' in post_dict else None
                     }

        projectid = Project.objects.get(pk=int(case_dict.get('projectid')))
        moduleid = Module.objects.get(pk=int(case_dict.get('moduleid')))
        testrailcaseid = case_dict.get('testrailcaseid')
        casedesc = case_dict.get('casedesc')
        if 'isenabled' in post_dict:
            isenabled = True
        else:
            isenabled = False
        if 'issmoke' in post_dict:
            issmoke = True
        else:
            issmoke = False
        dependent = case_dict.get('dependent')
        updateat = request.user.username
        updatetime = timezone.now()
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
        project = tcase.projectid
        projectlist = Project.objects.filter(productid=project.productid)
        keywordlist = Keyword.objects.filter(Q(productid=0)|Q(productid=project.productid.pk))
        elementlist = Element.objects.filter(projectid=project.pk)
        return render(request, 'testcase/caseedit.html', {'project':project,'modulelist':modulelist,'elementlist':elementlist,'projectlist':projectlist,'keywordlist':keywordlist,'steplist':steplist,'tcase':tcase})

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
                     "testrailcaseid": post_dict['testrailcaseid'] if 'testrailcaseid' in post_dict else None
                     }

        projectid = Project.objects.get(pk=int(case_dict.get('projectid')))
        moduleid = Module.objects.get(pk=int(case_dict.get('moduleid')))
        testrailcaseid = case_dict.get('testrailcaseid')
        casedesc = case_dict.get('casedesc')
        if 'isenabled' in post_dict:
            isenabled = True
        else:
            isenabled = False
        if 'issmoke' in post_dict:
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
        project = Project.objects.get(name=tcase.projectid.name)
        projectlist = Project.objects.filter(productid=project.productid)
        keywordlist = Keyword.objects.filter(Q(productid=0) | Q(productid=project.productid.pk))
        elementlist = Element.objects.filter(moduleid=tcase.moduleid)
        return render(request, 'testcase/casecopy.html', {'project':project,'modulelist':modulelist,'elementlist':elementlist,'projectlist':projectlist,'keywordlist':keywordlist,'steplist':steplist,'tcase':tcase})


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
    return render(request, 'testcase/caseview.html', locals())

class CaseListIndex(ListView):
    context_object_name = 'caselist'
    template_name = 'index.html'
    paginate_by = 10
    # raw_sql = "select * from autoplat_case where projectid_id in (select id from autoplat_project where productid_id in (select productname_id from autoplat_userandproduct where username_id=3));"
    casesum = 0
    model = Case
    http_method_names = [u'get']

    def get_queryset(self):
        prodcutid = UserAndProduct.objects.filter(username = self.request.user).values('productname')
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
        context['userandproduct'] = UserAndProduct.objects.all()
        context['casesum'] = self.casesum
        return context


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
