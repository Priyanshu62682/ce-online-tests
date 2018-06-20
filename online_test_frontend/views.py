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
		progress=request.POST['progress']
		data_input = json.loads(progress)
		new_input={data_input['question_num']:data_input['selected_choice']}

		exam_id=Exam.objects.get(id=request.POST['exam_id'])
		student=Student.objects.get(student_username=request.POST['student'])

		if Dynamic.objects.filter(student_id=student,test_id=exam_id).exists():
			current_progress=Dynamic.objects.get(student_id=student,test_id=exam_id)
			progress_old=current_progress.progress
			progress_old.update(new_input)
			current_progress.progress=progress_old
			current_progress.save()

		else:
			Dynamic.objects.create(
				student_id=student,
				test_id=exam_id,
				progress=new_input,
				)

	return HttpResponse('')

def calculate_SCC(question,choice_object_json,progress):
	# print(choice_object_json.choices)
	# print(progress['2'])
	# for answer in progress[question.serial]:
	# 	for correct in choice_object_json.correct_choice:
	# 		if answer==
	# print(question.serial)
	# print(progress[str(question.serial)])
	key = str(question.serial)
	if progress[key]==choice_object_json.correct_choice:
		marks = question.section.positive_marks
	else:
		marks = question.section.negative_marks
	
	print("Marks awarded: "+ str(marks))

	return marks
	# return 0

def calculate_MCC(question,choice_object_json,progress):
	key = str(question.serial)
	partial_correct=0
	for answer in progress[key]:
		if answer in choice_object_json.correct_choice:
			partial_correct+=1
		else:
			print("returned -ve")
			return question.section.negative_marks
	if partial_correct==len(choice_object_json.correct_choice):
		marks = question.section.positive_marks
	else:
		marks = question.section.per_option_positive_marks*partial_correct

	print("Multiple Correct"+ str(marks))
	return marks

def integer_choice_type(question,choice_object_json,progress):
	key = str(question.serial)
	if progress[key]==choice_object_json.correct_choice:
		marks = question.section.positive_marks
	else:
		marks = question.section.negative_marks
	
	print("Marks awarded: "+ str(marks))

	return marks

def Thank_view(request,student,exam_id):
	if request.method=='GET':
		student=Student.objects.get(student_username=student)
		exam_object = Exam.objects.get(id=exam_id)
		current_progress=Dynamic.objects.get(student_id=student,test_id=exam_object)
		progress=current_progress.progress
		student=current_progress.student_id
		test=current_progress.test_id
		
		result_object={}
		total_positives=0
		total_negatives=0
		total_positive_marks=0
		total_negative_marks=0
		total_score=0

		parts = Part.objects.filter(exam=exam_object)
		part_result_object=[]
		for part in parts:
			marks = 0
			positives = 0
			negatives = 0
			positive_marks = 0
			negative_marks = 0
			question_object = Question.objects.filter(exam=exam_object,part=part)
			for question in question_object:
				choice_object_json = QuestionChoices.objects.get(question_id=question)
				key = str(question.serial)
				temp_marks = 0
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
					elif str(question.section)=="integer_choice_type":
						temp_marks = calculate_IC(question,choice_object_json,progress)
					elif str(question.section)=="match_choice_type":
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
		result_object.update(final)
		#print(result_object)
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
	return render (request, 'online_test_frontend/thankyou.html', {'message': message,'progress':progress,
		'total_score':total_score})
