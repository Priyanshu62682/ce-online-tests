from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from django.views import generic
from django.forms import modelformset_factory
from .forms import *
from .models import *
from urllib import request
import json
from django.db import transaction
from operator import itemgetter


class DashboardView(generic.TemplateView):
	template_name = 'online_test/dashboard.html'

class TestListView(generic.ListView):
	model = Exam
	template_name = 'online_test/testslist.html'

class TestPartView(generic.DetailView):
	model = Exam
	template_name = 'online_test/testpartlist.html'
	slug_field = 'url'

	def get_context_data(self,**kwargs):
		context = super(TestPartView,self).get_context_data(**kwargs)
		# a query that selects all distinct values of part present in sections of that particular exam
		#context['parts'] = Section.objects.order_by('part').distinct('part')
		exam = Exam.objects.get(url=self.kwargs['slug'])
		context['exam'] =exam
		context['parts'] = Part.objects.filter(exam=exam)
		context['questions'] = Question.objects.filter(exam=exam)
		return context

class TestSectionListView(generic.ListView):
	model = Section
	template_name = 'online_test/listsections.html'

	def get_queryset(self,**kwargs):
		queryset = super(TestSectionListView, self).get_queryset(**kwargs)
		#part_name = self.kwargs['part']
		test_name = Exam.objects.get(url=self.kwargs['testslug'])
		try:
			part_object = Part.objects.get(exam=test_name,name=self.kwargs['part'])
		except:
			part_object=None
		queryset = Section.objects.filter(exam = test_name,part = part_object)
		return queryset
	def get_context_data(self,**kwargs):
		context = super(TestSectionListView,self).get_context_data(**kwargs)
		test_slug = self.kwargs['testslug']
		#part_name = self.kwargs['part']
		test_name = Exam.objects.get(url=test_slug)
		try:
			part_object = Part.objects.get(exam=test_name,name=self.kwargs['part'])
		except Part.DoesNotExist:
			part_object=None
		context['exam'] = test_name
		context['part'] = part_object
		context['questions'] = Question.objects.filter(exam=test_name,part=part_object)
		return context


class CreateTestView(CreateView):
	model = Exam
	fields = '__all__'
	template_name = 'online_test/createtest.html'

# class DynamicChoiceSubmit(CreateView):
# 	model = Dynamic
# 	fields = '__all__'

# 	def get_success_url(self, **kwargs):
# 		return reverse('online_test:testdetail',kwargs={'slug':self.kwargs['slug']})
	

# 	def get_context_data(self,**kwargs):
# 		context = super(DynamicChoiceSubmit,self).get_context_data(**kwargs)
# 		exam = Exam.objects.get(url=self.kwargs['slug'])
# 		context['exam'] =exam
# 		context['parts'] = Part.objects.filter(exam=exam)
# 		context['sections'] = Section.objects.filter(exam=exam)
# 		context['questions'] = Question.objects.filter(exam=exam)
# 		return context
		

def get_request_choice(request):
	if request.method=='POST':
		
		
		selected= request.POST['selected']
		exam_id=request.POST['exam_id']
		progress=request.POST['progress']
		me=Student.objects.get(student_username='Abhishek')

		# Dynamic.objects.get(student_id=me):
		current_progress=Dynamic.objects.get(student_id=me,test_id=exam_id)
		progress_old=current_progress.progress
		progress_oldJS=json.dumps(progress_old)

		# print(type(progress), type(progress_oldJS))
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

class CreatePartView(CreateView):
	template_name = 'online_test/newpart.html'
	model = Part
	fields = ('name',)

	def form_valid(self, form,**kwargs):
		form.instance.exam = Exam.objects.get(url=self.kwargs['testslug'])
		return super(CreatePartView, self).form_valid(form,**kwargs)

	def get_success_url(self,**kwargs):
		exam_instance = Exam.objects.get(url=self.kwargs['testslug'])
		return reverse('online_test:testdetail',kwargs={'slug':exam_instance.url })

	def get_context_data(self,**kwargs):
		context = super(CreatePartView,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(url=self.kwargs['testslug'])
		context['exam'] = exam_instance
		return context	


class CreateSectionView(CreateView):
	template_name = 'online_test/createnewsection.html'
	model = Section
	fields = ('positive_marks','per_option_positive_marks','negative_marks','section_instructions',)

	def form_valid(self, form,**kwargs):
		form.instance.exam = Exam.objects.get(title=self.kwargs['exam'])
		form.instance.part = Part.objects.get(exam=form.instance.exam,name=self.kwargs['part'])
		form.instance.section_type='single_choice_correct_type'
		return super(CreateSectionView, self).form_valid(form,**kwargs)

	def get_success_url(self,**kwargs):
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		return reverse('online_test:sections',kwargs={'testslug':exam_instance.url,'part':self.kwargs['part'] })

	def get_context_data(self,**kwargs):
		context = super(CreateSectionView,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		try:
			part_instance = Part.objects.get(exam=exam_instance,name=self.kwargs['part'])
		except Part.DoesNotExist:
			part_instance=None
		#part_instance = Part.objects.get(name=self.kwargs['part'])
		context['exam'] = exam_instance
		context['part'] = part_instance
		return context

class CreateMultipleSectionView(CreateView):
	template_name = 'online_test/createmultiplenewsection.html'
	model = Section
	fields = ('positive_marks','per_option_positive_marks','negative_marks','section_instructions',)
	
	def form_valid(self, form,**kwargs):
		form.instance.exam = Exam.objects.get(title=self.kwargs['exam'])
		form.instance.part = Part.objects.get(exam=form.instance.exam,name=self.kwargs['part'])
		form.instance.section_type='multiple_choice_correct_type'
		print('multiple_choice_correct_type')
		return super(CreateMultipleSectionView, self).form_valid(form,**kwargs)

	def get_success_url(self,**kwargs):
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		return reverse('online_test:sections',kwargs={'testslug':exam_instance.url,'part':self.kwargs['part'] })

	def get_context_data(self,**kwargs):
		context = super(CreateMultipleSectionView,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		try:
			part_instance = Part.objects.get(exam=exam_instance,name=self.kwargs['part'])
		except Part.DoesNotExist:
			part_instance=None
		#part_instance = Part.objects.get(name=self.kwargs['part'])
		context['exam'] = exam_instance
		context['part'] = part_instance
		return context

class CreateMatchSectionView(CreateView):
	template_name = 'online_test/creatematchsection.html'
	model = Section
	fields = ('positive_marks','per_option_positive_marks','negative_marks','section_instructions',)
	
	def form_valid(self, form,**kwargs):
		form.instance.exam = Exam.objects.get(title=self.kwargs['exam'])
		form.instance.part = Part.objects.get(exam=form.instance.exam,name=self.kwargs['part'])
		form.instance.section_type='match_type'
		print('match')
		return super(CreateMatchSectionView, self).form_valid(form,**kwargs)

	def get_success_url(self,**kwargs):
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		return reverse('online_test:sections',kwargs={'testslug':exam_instance.url,'part':self.kwargs['part'] })

	def get_context_data(self,**kwargs):
		context = super(CreateMatchSectionView,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		try:
			part_instance = Part.objects.get(exam=exam_instance,name=self.kwargs['part'])
		except Part.DoesNotExist:
			part_instance=None
		#part_instance = Part.objects.get(name=self.kwargs['part'])
		context['exam'] = exam_instance
		context['part'] = part_instance
		return context

class CreateIntegerSectionView(CreateView):
	template_name = 'online_test/createintegersection.html'
	model = Section
	fields = ('positive_marks','per_option_positive_marks','negative_marks','section_instructions',)
	
	def form_valid(self, form,**kwargs):
		form.instance.exam = Exam.objects.get(title=self.kwargs['exam'])
		form.instance.part = Part.objects.get(exam=form.instance.exam,name=self.kwargs['part'])
		form.instance.section_type='integer_type'
		print('integer_type')
		return super(CreateIntegerSectionView, self).form_valid(form,**kwargs)

	def get_success_url(self,**kwargs):
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		return reverse('online_test:sections',kwargs={'testslug':exam_instance.url,'part':self.kwargs['part'] })

	def get_context_data(self,**kwargs):
		context = super(CreateIntegerSectionView,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		try:
			part_instance = Part.objects.get(exam=exam_instance,name=self.kwargs['part'])
		except Part.DoesNotExist:
			part_instance=None
		#part_instance = Part.objects.get(name=self.kwargs['part'])
		context['exam'] = exam_instance
		context['part'] = part_instance
		return context

class AddQuestionViewBatch(CreateView):
	#model = Question
	#fields = ('content','figure',)
	#template_name = 'online_test/newquestion.html'
	form_class = QuestionForm
	template_name = 'online_test/testquestion.html'

	def get_context_data(self,**kwargs):
		context = super(AddQuestionViewBatch,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		part_instance = Part.objects.get(exam=exam_instance,name=self.kwargs['part'])
		section_instance = Section.objects.get(exam=exam_instance, part=part_instance,section_type=self.kwargs['section'])
		context['exam'] = self.kwargs['exam']
		context['part'] = self.kwargs['part']
		context['section'] = self.kwargs['section']
		context['formset'] = QuestionFormset(queryset=Question.objects.none())
		return context

	def post(self, request, *args, **kwargs):
		formset = QuestionFormset(request.POST)
		if formset.is_valid():
			return self.form_valid(formset)

	def form_valid(self, formset,**kwargs):
		for form in formset:
			form.instance.exam = Exam.objects.get(title=self.kwargs['exam'])
			form.instance.part = Part.objects.get(exam=form.instance.exam,name=self.kwargs['part'])
			form.instance.section = Section.objects.get(
				exam=form.instance.exam, part=form.instance.part,section_type=self.kwargs['section'])
		formset.save()
		return super(AddQuestionViewBatch, self).form_valid(form,**kwargs)

	def get_success_url(self,**kwargs):
		return reverse('online_test:updatesection',
			kwargs={'exam':self.kwargs['exam'],'part':self.kwargs['part'],'section':self.kwargs['section'] })

	# def form_valid(self, formset):
	# 	formset.save()
	# 	return HttpResponseRedirect('/dashboard/managetests/')

class AddQuestionView(CreateView):
	model = Question
	fields = ('content','figure',)
	template_name = 'online_test/newquestion.html'

	def get_context_data(self,**kwargs):
		context = super(AddQuestionView,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		part_instance = Part.objects.get(exam=exam_instance,name=self.kwargs['part'])
		section_instance = Section.objects.get(exam=exam_instance, part=part_instance,section_type=self.kwargs['section'])
		context['exam'] = self.kwargs['exam']
		context['part'] = self.kwargs['part']
		context['section'] = self.kwargs['section']
		# context['formset'] = QuestionFormset(queryset=Question.objects.none())
		return context

	def form_valid(self, form,**kwargs):
		form.instance.exam = Exam.objects.get(title=self.kwargs['exam'])
		form.instance.part = Part.objects.get(exam=form.instance.exam,name=self.kwargs['part'])
		form.instance.section = Section.objects.get(
			exam=form.instance.exam, part=form.instance.part,section_type=self.kwargs['section'])
		return super(AddQuestionView, self).form_valid(form,**kwargs)

	def get_success_url(self,**kwargs):
		return reverse('online_test:updatesection',
			kwargs={'exam':self.kwargs['exam'],'part':self.kwargs['part'],'section':self.kwargs['section'] })


	
class SectionUpdateView(generic.TemplateView):
	model = Section
	template_name = 'online_test/sectiondetail.html'

	def get_context_data(self,**kwargs):
		context = super(SectionUpdateView,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		part_instance = Part.objects.get(exam=exam_instance,name=self.kwargs['part'])
		section_instance = Section.objects.get(exam=exam_instance, part=part_instance,section_type=self.kwargs['section'])
		context['exam'] = exam_instance
		context['part'] = part_instance
		context['section'] = section_instance		
		context['questions'] = Question.objects.filter(
			exam=exam_instance,
			part=part_instance,
			section=section_instance)
		return context

class AddNewChoices(CreateView):
	model = SingleChoiceCorrect
	fields = ('choice_1','choice_2','choice_3','choice_4','correct_choice')
	template_name = 'online_test/newchoices.html'
	# def get_initial(self,**kwargs):
	# 	exam_instance = Exam.objects.get(title=self.kwargs['exam'])
	# 	part_instance = Part.objects.get(exam=exam_instance, name=self.kwargs['part'])
	# 	section_instance = Section.objects.get(exam=exam_instance, part=part_instance,section_type=self.kwargs['section'])
	# 	return {'exam': exam_instance,
	# 	'part': part_instance,
	# 	'section':section_instance}

	def form_valid(self, form,**kwargs):
		form.instance.question_id = Question.objects.get(id=self.kwargs['question'])
		return super(AddNewChoices, self).form_valid(form,**kwargs)

	def get_success_url(self,**kwargs):
		return reverse('online_test:updatesection',
			kwargs={'exam':self.kwargs['exam'],'part':self.kwargs['part'],'section':self.kwargs['section'] })

	def get_context_data(self,**kwargs):
		context = super(AddNewChoices,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		part_instance = Part.objects.get(exam=exam_instance,name=self.kwargs['part'])
		section_instance = Section.objects.get(exam=exam_instance, part=part_instance,section_type=self.kwargs['section'])
		question_instance = Question.objects.get(id=self.kwargs['question'])
		context['exam'] = exam_instance
		context['part'] = part_instance
		context['section'] = section_instance	
		context['question'] = question_instance
		return context

class AuthorDelete(DeleteView):
    model = Question

    def get_success_url(self, **kwargs):
    	return reverse('online_test:updatesection',
			kwargs={'exam':self.kwargs['exam'],'part':self.kwargs['part'],'section':self.kwargs['section']})

    def get_context_data(self,**kwargs):
    	context = super(AuthorDelete,self).get_context_data(**kwargs)
    	exam_instance = Exam.objects.get(title=self.kwargs['exam'])
    	part_instance = Part.objects.get(exam=exam_instance,name=self.kwargs['part'])
    	section_instance = Section.objects.get(exam=exam_instance, part=part_instance,section_type=self.kwargs['section'])
    	context['exam'] = exam_instance
    	context['part'] = part_instance
    	context['section'] = section_instance		
    	context['questions'] = Question.objects.filter(
			exam=exam_instance,
			part=part_instance,
			section=section_instance)
    	return context	

class PartDelete(DeleteView):
    model = Part

    def get_success_url(self, **kwargs):
    	return reverse('online_test:testdetail',
			kwargs={'slug':self.kwargs['slug']})

    def get_context_data(self,**kwargs):
    	context = super(PartDelete,self).get_context_data(**kwargs)
    	exam = Exam.objects.get(url=self.kwargs['slug'])
    	context['exam'] =exam
    	context['parts'] = Part.objects.filter(exam=exam)
    	context['sections'] = Section.objects.filter(exam=exam)
    	context['questions'] = Question.objects.filter(exam=exam)
    	return context 

class TestDelete(DeleteView):
	model=Exam

	def get_success_url(self, ** kwargs):
		return reverse('online_test:testmanage')

class ResultListView(generic.TemplateView):
	template_name = 'online_test/testresults.html'

	def get_context_data(self,**kwargs):
		context = super(ResultListView,self).get_context_data(**kwargs)
		tests = Exam.objects.filter(test_completed=True)
		print(tests)
		context['tests'] = tests
		return context

class ResultDetailView(generic.TemplateView):
	template_name = 'online_test/singletestresult.html'

	def get_context_data(self,**kwargs):
		context = super(ResultDetailView,self).get_context_data(**kwargs)


		exam = Exam.objects.get(title=self.kwargs['exam'])
		students = Result.objects.filter(test_id=exam)
		context['exam'] = Exam.objects.get(title=self.kwargs['exam'])
		context['students'] = students
		print(students)
		return context

class QuestionChoiceAdd(CreateView):
    model = Question
    fields = ['serial','content', 'figure']
    extra=2

    def get_context_data(self, **kwargs):
    	context=super(QuestionChoiceAdd,self).get_context_data(**kwargs)
    	exam_instance = Exam.objects.get(title=self.kwargs['exam'])
    	part_instance = Part.objects.get(exam=exam_instance,name=self.kwargs['part'])
    	section_instance = Section.objects.get(exam=exam_instance, part=part_instance,section_type=self.kwargs['section'])
    	context['exam'] = self.kwargs['exam']
    	context['part'] = self.kwargs['part']
    	context['section'] = self.kwargs['section']

    	if self.request.POST:
    		context['formset']=QuestionAddForm(self.request.POST)
    	else:
    		if context['section']=='single_choice_correct_type':
	    		context['formset']=QuestionAddForm(extra=4)
	    	if  context['section']=='multiple_choice_correct_type':
	    		context['formset']=QuestionAddForm(extra=4)
	    	if context['section']=='match_type':
	    		context['formset']=QuestionAddForm(extra=5)
	    	if context['section']=='integer_type':
	    		context['formset']=QuestionAddForm(extra=0)


    	return context

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.exam = Exam.objects.get(title=self.kwargs['exam'])
        form.instance.part = Part.objects.get(exam=form.instance.exam,name=self.kwargs['part'])
        form.instance.section = Section.objects.get(exam=form.instance.exam, part=form.instance.part,section_type=self.kwargs['section'])
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()

            formset.instance = self.object
            question_id=self.request.POST.getlist("question_id")

            print(question_id)
            # cd = formset.cleaned_data
            if context['section']=='single_choice_correct_type' or context['section']=='multiple_choice_correct_type':
            	c_1=self.request.POST.getlist("choice_1")
            	c_2=self.request.POST.getlist("choice_2")
            	c_3=self.request.POST.getlist("choice_3")
            	c_4=self.request.POST.getlist("choice_4")
            	c_a=self.request.POST.getlist("correct_choice")
            	answer=	[]
            	answer.append(c_1[0])
            	answer.append(c_2[0])
            	answer.append(c_3[0])
            	answer.append(c_4[0])
            	# print(answer)
            	member = QuestionChoices(choices=answer, correct_choice=c_a, question_id=formset.instance, section=form.instance.section)
            	member.save()
            else:
            	if context['section']=='match_type':
            		c_1=self.request.POST.getlist("choice_1")
            		c_2=self.request.POST.getlist("choice_2")
            		c_3=self.request.POST.getlist("choice_3")
            		c_4=self.request.POST.getlist("choice_4")
            		c_5=self.request.POST.getlist("choice_5")
            		c_a=self.request.POST.getlist("correct_choice")
            		answer=[]
            		answer.append(c_1[0])
            		answer.append(c_2[0])
            		answer.append(c_3[0])
            		answer.append(c_4[0])
            		answer.append(c_5[0])

            		member = QuestionChoices(choices=answer, correct_choice=c_a, question_id=formset.instance, section=form.instance.section)
            		member.save()

            	else:
            		c_1=self.request.POST.getlist("choice_1")
            		c_a=self.request.POST.getlist("correct_choice")
            		answer=[]
            		member = QuestionChoices(choices=answer, correct_choice=c_a, question_id=formset.instance, section=form.instance.section)
            		member.save()

            # formset.save()
            return HttpResponseRedirect(reverse('online_test:updatesection', 
            	kwargs={'exam':self.kwargs['exam'], 'part':self.kwargs['part'], 'section':self.kwargs['section']}))
        else:
            return self.render_to_response(self.get_context_data(form=form))




    def get_success_url(self,**kwargs):
    	return HttpResponseRedirect(reverse('online_test:updatesection',
    		kwargs={'exam':self.kwargs['exam'],'part':self.kwargs['part'],'section':self.kwargs['section'] }))
    # if this is POST request we need to process the form data
	
	# examobj=Exam.objects.get(title=exam)
	# partobj=Part.objects.get(exam=examobj, name=part)
	# sectionobj=Section.objects.get(exam=examobj, part=partobj, section_type=section)




	# question=Question()
	# choice=QuestionChoices()

	

	# if request.method == 'POST':

		
	# 	# create a form instance and populate it with data from the request:
	# 	form_question = QuestionAddFormset(request.POST)
	# 	form_choice = ChoiceAddFormset(request.POST)

	#     # check whether it's valid:
	# 	if form_question.is_valid() and form_choice.is_valid():

	# 		# Save User model fields
	# 		question.exam=examobj
	# 		question.part=partobj
	# 		question.section=sectionobj
	# 		question.content = request.POST['content']
	# 		question.serial = request.POST['serial']
	# 		# user.last_name = request.POST['last_name']
	# 		question.save()

	# 		# Save Employee model fields
	# 		choice.question_id=question
	# 		choice.section=sectionobj
	# 		choice.choices = request.POST['choices']
			

	# 		choice.save() 

	# 		# redirect to the index page
	# 		return HttpResponseRedirect(reverse('online_test:updatesection',
	# 			kwargs={'exam':exam,'part':part,'section':section }))

	# # if a GET (or any other method) we'll create a blank form
	# else:

	# 	form_question = QuestionAddFormset(queryset=Question.objects.none())
	# 	form_choice = ChoiceAddFormset(queryset=Question.objects.none())

	# return render(request, 'online_test/question_form.html', {'form_question': form_question, 'form_choice': form_choice})
	






