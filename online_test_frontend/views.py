from django.shortcuts import render
from django.views import generic
from online_test.models import *
from online_test_frontend.models import *
from rest_framework.views import APIView,Response
from online_test.serializers import *

# Create your views here.

class UserDashboardView(generic.TemplateView):
	template_name = 'online_test_frontend/dashboard.html'
	def get_context_data(self,**kwargs):
		context = super(UserDashboardView,self).get_context_data(**kwargs)
		#Select exam as per convinience
		user = Student.objects.get(student_username=self.kwargs['student'])
		print(user)
		context['student'] = self.kwargs['student']
		context['active_tests'] = Exam.objects.filter(published=True)
		context['registered_tests'] = Subscriptions.objects.filter(student=user)
		return context

class TakeTestView(generic.TemplateView):
	template_name = 'online_test_frontend/taketest.html'
	def get(self,request,student,exam):
		exam = Exam.objects.filter(title=exam)
		serializer = ExamSerializer(instance=exam,many=True)
		#print(serializer.data)
		#return Response(serializer.data)
		return render(request, self.template_name, {'test': serializer.data})

	# def get_context_data(self,**kwargs):
	# 	context = super(TakeTestView,self).get_context_data(**kwargs)
	# 	exam = Exam.objects.filter(title=self.kwargs['exam'])
	# 	serializer = ExamSerializer(instance=exam,many=True)
	# 	context['testdata'] = serializer.data
	# 	print(serializer.data)
	# 	return context

class TestView(APIView):
	def get(self,request,student,exam):
		album = Album.objects.get(album_name='The Grey Album')
		
		serializer = AlbumSerializer(album,many=True)
		return Response(serializer.data)