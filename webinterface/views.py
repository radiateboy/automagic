from django.http import HttpResponse
from django.shortcuts import render
from webinterface.models import *
from django.views.generic import ListView
from autoplat.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
# Create your views here.

class WebinterfaceListIndex(ListView):
	context_object_name = 'caselist'
	template_name = 'webinterface.html'
	paginate_by = 10
	# raw_sql = "select * from autoplat_case where projectid_id in (select id from autoplat_project where productid_id in (select productname_id from autoplat_userandproduct where username_id=3));"
	casesum = 0
	model = Webinterface
	http_method_names = [u'get']

	def get_queryset(self):
		prodcutid = UserandProduct.objects.filter(username = self.request.user).values('productname')
		caselist = Webinterface.objects.filter(projectid__in=Project.objects.filter(productid__in=prodcutid).values('id')).order_by('-pk')
		prodcutid = self.request.GET.get('check_productname')
		projectid = self.request.GET.get('projectid')
		moduleid = self.request.GET.get('moduleid')
		casestatus = self.request.GET.get('casestatus')
		keyword = self.request.GET.get('keyword')
		if prodcutid and int(prodcutid):
			caselist = caselist.filter(projectid__in=Project.objects.filter(productid=prodcutid).values('id'))
		if projectid:
			caselist = caselist.filter(projectid=projectid)
		if moduleid:
			caselist = caselist.filter(moduleid=moduleid)
		if casestatus:
			caselist = caselist.filter(isenabled=casestatus)
		if keyword:
			caselist = caselist.filter(Q(pk__icontains=keyword)|Q(descr=keyword)|Q(createat__icontains=keyword))
		self.casesum = len(caselist)
		return caselist

	def get_context_data(self, **kwargs):
		projectid = self.request.GET.get('projectid')
		context = super(WebinterfaceListIndex,self).get_context_data(**kwargs)
		# namelist = Case.objects.values('casedesc').annotate()
		# context['casedesc'] = namelist
		context['projectlist'] = Project.objects.all().order_by('-sortby')
		context['modulelist'] = Module.objects.all().order_by('-sortby')
		# context['productlist'] = Product.objects.all().order_by('-sortby')
		context['userandproduct'] = UserandProduct.objects.all()
		# context['casedata'] = Webresponse.objects.all()
		context['casesum'] = self.casesum
		return context

@login_required()
def get_response(request):
	responsedata = []
	webinterfaceid = request.GET['webinterfaceid']
	datalist = Webresponse.objects.filter(webinterfaceid=webinterfaceid)
	for i in datalist:
		responseinfo = {}
		responseinfo['id'] = i.id
		responseinfo['params'] = i.params
		responseinfo['exectime'] = i.exectime
		responseinfo['expected'] = i.expected
		responseinfo['actual'] = i.actual
		responseinfo['status_code'] = i.status_code
		responseinfo['Response_content'] = i.Response_content
		responsedata.append(responseinfo)
	return HttpResponse(json.dumps(responsedata))