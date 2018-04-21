from django.shortcuts import render
from django.views import generic
from online_test.models import *
from online_test_frontend.models import *
# Create your views here.

class UserDashboardView(generic.TemplateView):
	template_name = 'online_test_frontend/dashboard.html'

	def get_context_data(self,**kwargs):

		context = super(UserDashboardView,self).get_context_data(**kwargs)
		#Select exam as per convinience
		user = Student.objects.get(student_username=self.kwargs['user'])
		print(user)
		context['active_tests'] = Exam.objects.filter(published=True)
		context['registered_tests'] = Subscriptions.objects.filter(student=user)
		return context
