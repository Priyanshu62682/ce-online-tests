from django.shortcuts import render
from django.views import generic
from online_test.models import *
from online_test_frontend.models import *
from rest_framework.views import APIView,Response
from online_test.serializers import *
from django.http import JsonResponse
from django.http import HttpResponse,HttpResponseRedirect
import json
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from datetime import datetime
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect

# Create your views here.

class UserDashboardView(generic.TemplateView):
	template_name = 'online_test_frontend/dashboard.html'
	def get_context_data(self,**kwargs):
		context = super(UserDashboardView,self).get_context_data(**kwargs)
		#Select exam as per convinience

		user = Student.objects.get(student_username=self.kwargs['student'])
		context['student'] = self.kwargs['student']
		registered_tests = Subscriptions.objects.filter(student=user)
		context['registered_tests'] = registered_tests
		context['active_tests'] = Exam.objects.filter(published=True).exclude(
			title__in=[test.exam for test in registered_tests])
		
		return context

#class TakeTestView(APIView):
class TakeTestView(generic.TemplateView):
	template_name = 'online_test_frontend/taketest.html'
	def get(self,request,student,exam):
		exam = Exam.objects.filter(title=exam)
		student_instance=Student.objects.get(student_username=student)
		if Result.objects.filter(test_id=exam.first(), student_username=student_instance).exists():
			return HttpResponse('<center><h3>Sorry! You already have taken this Test.</h3></center>')
			# raise Http404("Sorry! You already have taken this Test.")
			# raise PermissionDenied
			# return render(request, 'online_test_frontend/dashboard.html')
		context = {
			"exam":exam,
			"student":student_instance,
		}
		serializer = ExamSerializer(instance=exam,context=context,many=True)
		#print(serializer.data)
		#return Response(serializer.data[0])
		return render(request, self.template_name, {'test': serializer.data[0],'student':student_instance, 'exam':exam.first() })

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
		progress=request.POST['progress']
		data_input = json.loads(progress)
		new_input={
			str(data_input['questionNumber']):str(data_input['choice'])
		}
		new_state = {
			str(data_input['questionNumber']):str(data_input['state'])
		}
		#to be reversed from frontend
		sid = request.POST['exam_id']
		eid = request.POST['student']
		exam_id=Exam.objects.get(id=eid)
		student=Student.objects.get(student_username=sid)

		if Dynamic.objects.filter(student_id=student,test_id=exam_id).exists():
			current_progress=Dynamic.objects.get(student_id=student,test_id=exam_id)
			progress_old=current_progress.progress
			progress_old_state=current_progress.progress_state
			key = str(data_input['questionNumber'])
			progress_old.update(new_input)
			progress_old_state.update(new_state)
			current_progress.progress=progress_old
			current_progress.progress_state=progress_old_state
			current_progress.save()

		else:
			Dynamic.objects.create(
				student_id=student,
				test_id=exam_id,
				progress=new_input,
				progress_state=new_state,
				)

	else:
		return HttpResponse('Get Called')
	return HttpResponse('')

def calculate_SCC(question,choice_object_json,progress):

	key = str(question.serial)
	if progress[key]==choice_object_json.correct_choice:
		marks = question.section.positive_marks
	else:
		marks = question.section.negative_marks

	return marks

def calculate_MCC(question,choice_object_json,progress):
	key = str(question.serial)
	#print('Inside MCQ')
	partial_correct=0
	for answer in progress[key]:
		#print(answer)
		#print(choice_object_json.correct_choice)
		if answer in choice_object_json.correct_choice:
			partial_correct+=1
			#print('Added correct partial')
		else:
			#print("returned -ve")
			return question.section.negative_marks
	if partial_correct==len(choice_object_json.correct_choice):
		marks = question.section.positive_marks
	else:
		marks = question.section.per_option_positive_marks*partial_correct

	#print("Multiple Correct"+ str(marks))
	return marks

def integer_choice_type(question,choice_object_json,progress):
	key = str(question.serial)
	if progress[key]==choice_object_json.correct_choice:
		marks = question.section.positive_marks
	else:
		marks = question.section.negative_marks
	
	#print("Marks awarded: "+ str(marks))

	return marks

def calculate_performance(question_object,progress):
	performance = []
	for question in question_object:
		choice_object_json = QuestionChoices.objects.get(question_id=question).choices
		marked_choice = progress[str(question.serial)]
		

def Thank_view(request,student,exam_id):
	print("In here")
	if request.method=='GET':
		student=Student.objects.get(student_username=student)
		exam_object = Exam.objects.get(id=exam_id)
		current_progress=Dynamic.objects.get(student_id=student,test_id=exam_object)
		print(exam_object)

		progress=current_progress.progress
		student=current_progress.student_id
		print(progress)
		print(student)
		test=current_progress.test_id
		
		result_object={}
		total_positives=0
		total_negatives=0
		total_positive_marks=0
		total_negative_marks=0
		total_score=0

		parts = Part.objects.filter(exam=exam_object)
		part_result_object=[]
		performance = []
		for part in parts:
			marks = 0
			positives = 0
			negatives = 0
			positive_marks = 0
			negative_marks = 0
			question_object = Question.objects.filter(exam=exam_object,part=part).order_by('serial')		

			for question in question_object:

				temp_performance = []

				choice_object_json = QuestionChoices.objects.get(question_id=question)
				key = str(question.serial)
				temp_marks = 0

				#performance object calculation
				
				temp_performance.append(question.serial)
				save_progress = ', '.join(progress[key])
				save_correct_choice = ', '.join(choice_object_json.correct_choice)
				temp_performance.append(save_progress)
				temp_performance.append(save_correct_choice)

				# print(question.correct_choice)
				# print(progress[key])
				# print(str(question.section))

				# checks if answer is marked by the student 
				# (if answer of corresponding question from all questions, is present in Dynamic object)
				if key in progress:
					# print(str(question.section))
					if str(question.section)=="single_choice_correct_type":
						temp_marks = calculate_SCC(question,choice_object_json,progress)
					elif str(question.section)=="multiple_choice_correct_type":
						temp_marks = calculate_MCC(question,choice_object_json,progress)
					elif str(question.section)=="integer_type":
						temp_marks = calculate_IC(question,choice_object_json,progress)
					elif str(question.section)=="match_type":
						temp_marks = calculate_MatchCT(question,choice_object_json,progress)
					else:
						temp_marks = 0
						#print('Nothing')

					if temp_marks > 0:
						positives+=1
						positive_marks += temp_marks
					else:
						negatives+=1
						negative_marks += temp_marks

					temp_performance.append(temp_marks)
					# print(temp_performance)
					performance.append(temp_performance)

			total_positives+=positives
			total_negatives+=negatives
			total_positive_marks+=positive_marks
			total_negative_marks+=negative_marks
			

			#print(positive_marks)
			#print(negative_marks)
			part_result = {
				'name': part.name,
				'positives': positives,
				'negatives': negatives,
				'positive_marks':positive_marks,
				'negative_marks': negative_marks,
				'score': positive_marks+negative_marks
			}
			part_result_object.append(part_result)

		total_score+=total_positive_marks+total_negative_marks
		final = {
			'total_positives': total_positives,
			'total_negatives': total_negatives,
			'total_positive_marks': total_positive_marks,
			'total_negative_marks': total_negative_marks,
			'total_score': total_score
		}
		result_object.update({'part_result':part_result_object})
		
		result_object.update({'user_choices':current_progress.progress})
		result_object.update(final)

		if not Result.objects.filter(test_id=test,student_username=student).exists():
			Result.objects.create(
				test_completed= True,
				test_id=test,
				student_username=student,
				result_json=result_object,
				)
			current_progress.delete()
			message = 'Thank you for taking the test'
		else:
			message = 'Already submitted'
			progress = {}
			total_score = 'None'


		# question_object = Question.objects.filter(exam=exam_object).order_by('serial')
	return render (request, 'online_test_frontend/thankyou.html', {'message': message,'progress':progress,
		'total_score':total_score,'performance':performance})

class UserTestInfo(generic.TemplateView):
	template_name = 'online_test_frontend/usertestinfo.html'
	def get_context_data(self,**kwargs):
		context = super(UserTestInfo,self).get_context_data(**kwargs)
		#Select exam as per convinience
		user = Student.objects.get(student_username=self.kwargs['student'])
		context['student'] = self.kwargs['student']
		context['exam'] = Exam.objects.get(title=self.kwargs['exam'])
		return context
		


class SubscribeTest(CreateView):
	template_name = 'online_test_frontend/confirm_registration.html'
	model = Subscriptions
	fields = '__all__'

	# def form_valid(self, form,**kwargs):

	# 	student = Student.objects.get(student_username=self.kwargs['student'])
	# 	exam = Exam.objects.get(title=self.kwargs['exam'])
	# 	form.instance.student = student
	# 	form.instance.exam = exam
	# 	form.instance.event = 'Upcoming'
	# 	form.instance.registered_on = datetime.now
	# 	return super(SubscribeTest, self).form_valid(form,**kwargs)

	def get(self, request, *args, **kwargs):
		exam = Exam.objects.filter(title=self.kwargs['exam']).first()
		student = Student.objects.filter(student_username=self.kwargs['student']).first()
		if Subscriptions.objects.filter(student=student,exam=exam).exists():
			return HttpResponseRedirect(reverse('online_test_frontend:user-dashboard', kwargs={'student':student}))
		else:
			return super(SubscribeTest, self).get(self,request,**kwargs)


	def get_context_data(self,**kwargs):
		context = super(SubscribeTest,self).get_context_data(**kwargs)
		#Select exam as per convinience
		context['student'] = self.kwargs['student']
		context['exam'] = self.kwargs['exam']
		return context

	def get_initial(self):
		exam = Exam.objects.filter(title=self.kwargs['exam']).first()
		student = Student.objects.filter(student_username=self.kwargs['student']).first()
		initial_data = super(SubscribeTest, self).get_initial()
		initial_data['student'] = student
		initial_data['exam'] = exam
		return initial_data

	def get_success_url(self,**kwargs):
		return reverse('online_test_frontend:usertestinfo',
			kwargs={'student':self.kwargs['student'],'exam':self.kwargs['exam'] })

