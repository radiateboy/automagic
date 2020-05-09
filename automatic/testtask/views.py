# -*- coding:utf-8 -*-
"""
__author__ = 'Ray'
mail:tsbc@vip.qq.com
2020-01-06
"""
import logging, json, os
import jenkins
import time
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.db.models import Q
from django.urls import reverse
from automatic.testcase.models import Case
from automatic.management.models import Product,Project,Module,User,UserAndProduct
from automatic.testtask.models import Task, Taskhistory, Codelist
# Create your views here.


# fixed #27
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
# fixed #27

class TaskListIndex(ListView):
	context_object_name = 'tasklist'
	template_name = 'testtask/tasklist.html'
	paginate_by = 10
	# raw_sql = "select * from autoplat_case where projectid_id in (select id from autoplat_project where productid_id in (select productname_id from autoplat_userandproduct where username_id=3));"
	tasksum = 0
	queryset = Task.objects.filter(projectid=3)
	http_method_names = [u'get']

	def get_queryset(self):
		tasklist = Task.objects.all().order_by('-pk')
		prodcutid = UserAndProduct.objects.filter(username=self.request.user).values('productname')
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
		context['userandproduct'] = UserAndProduct.objects.all()
		return context


@csrf_exempt
@login_required()
def add_task(request):
	if request.method == 'POST':
		post_dict = request.POST
		taskname = post_dict['taskname']
		runid = post_dict['testrailrunid'] if 'testrailrunid' in post_dict else None
		sectionid = post_dict['testsectionid'] if 'testsectionid' in post_dict else None
		suitesid = post_dict['testrailsuites'] if 'testsectionid' in post_dict else None
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
		if 'codename' in post_dict:
			codename_list,codedescr_list, codevalue_list = post_dict.getlist("codename"),post_dict.getlist("codedescr"), post_dict.getlist("codevalue")
			for codename, codedescr, codevalue in zip(codename_list, codedescr_list, codevalue_list):
					task.codelist_set.create(codedescr=codedescr, codename=codename, codevalue=codevalue)
		return HttpResponse('任务创建成功')
	else:
		userandproduct = UserAndProduct.objects.all()
		projectlist = Project.objects.all().order_by('-sortby')
		modulelist = Module.objects.all().order_by('-sortby')
		caselist =  Case.objects.filter(isenabled=True)
		return render(request, 'testtask/taskadd.html',{'userandproduct':userandproduct,'projectlist':projectlist,'modulelist':modulelist,'caselist':caselist})

@csrf_exempt
@login_required()
def update_task(request,id):
	taskinfo = Task.objects.get(pk=id)
	project = Project.objects.get(pk=taskinfo.projectid.pk)
	# print(project)
	if request.method == 'POST':
		post_dict = request.POST
		taskname = post_dict['taskname']
		testrailrunid = post_dict['testrailrunid'] if 'testrailrunid' in post_dict else None
		testsectionid = post_dict['testsectionid'] if 'testsectionid' in post_dict else None
		suitesid = post_dict['testrailsuites'] if 'testrailsuites' in post_dict else None
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
		updatetime = timezone.now()
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
		userandproduct = UserAndProduct.objects.all()
		projectlist = Project.objects.filter(productid=project.productid).order_by('-sortby')
		modulelist = Module.objects.all().order_by('-sortby')
		caselist =  Case.objects.filter(isenabled=True)
		taskcase = taskinfo.caselist
		codelist = Codelist.objects.filter(taskid=id)
		casesum = len(taskcase.split(','))
		return render(request, 'testtask/taskedit.html',{'taskinfo':taskinfo,'codelist':codelist, 'casesum':casesum, 'userandproduct':userandproduct,'projectlist':projectlist,'modulelist':modulelist,'caselist':caselist})

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
		starttime = timezone.now()
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
		starttime = timezone.now()
		server.build_job(build_name)
		task.status=1
		task.save()
		# build_num = jenkins.get_nextBuildNumber()
		# th = Taskhistory(taskid=task, userid=request.user, tasktype='3', taskname=task.taskname, starttime=starttime, build_name=task.build_name, build_number=build_num)
		# th.save()
	return HttpResponseRedirect(reverse('tasklist'))

@login_required()
def set_tree_task(request):
	taskid = request.GET['taskid']
	task = Task.objects.get(pk=taskid)
	# print elementinfo['projectid'],elementinfo['moduleid'],elementinfo['locmode']
	return HttpResponse(task.caselist)

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
