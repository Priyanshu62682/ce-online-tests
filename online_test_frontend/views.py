from django.shortcuts import render
from django.views import generic
from online_test.models import *
from online_test_frontend.models import *
from rest_framework.views import APIView,Response
from online_test.serializers import *
from django.http import JsonResponse
from django.http import HttpResponse,HttpResponseRedirect
import json

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
		student_instance=Student.objects.get(student_username=student)
		#print(serializer.data)
		#return Response(serializer.data)
		return render(request, self.template_name, {'test': serializer.data,'student':student_instance})

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


def get_request_choice(request):
	if request.method=='POST':
		
		
		# selected= request.POST['selected']
		exam_id=request.POST['exam_id']
		progress=request.POST['progress']
		me=Student.objects.get(student_username='Priyanshu')

		# Dynamic.objects.get(student_id=me):
		current_progress=Dynamic.objects.get(student_id=me,test_id=exam_id)
		progress_old=current_progress.progress

		progress_oldJS=json.dumps(progress_old)
		progress_new=progress+progress_oldJS
		
		current_progress.progress=progress_new
		current_progress.save()

		# else:
		# 	Dynamic.objects.create(
		# 		student_id=me,
		# 		test_id=exam_id,
		# 		progress=progress,
		# 		)

	return HttpResponse('')


def Thank_view(request,student,exam_id):
	if request.method=='GET':
		student=Student.objects.get(student_username=student)
		current_progress=Dynamic.objects.get(student_id=student,test_id=exam_id)
		progress=current_progress.progress
		student=current_progress.student_id
		test=current_progress.test_id

		Result.objects.create(
			test_completed= True,
			test_id=test,
			student_username=student,
			result_json=progress,

			)
	return render (request, 'online_test_frontend/thankyou.html', {'progress':progress})
