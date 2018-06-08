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
		context['sections'] = Section.objects.filter(exam=exam)
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
		return context


class CreateTestView(CreateView):
	model = Exam
	fields = '__all__'
	template_name = 'online_test/createtest.html'
		

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
	fields = ('section_type','positive_marks','negative_marks','section_instructions',)

	def form_valid(self, form,**kwargs):
		form.instance.exam = Exam.objects.get(title=self.kwargs['exam'])
		form.instance.part = Part.objects.get(exam=form.instance.exam,name=self.kwargs['part'])
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

	# def form_valid(self, formset):
	# 	formset.save()
	# 	return HttpResponseRedirect('/dashboard/managetests/')

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
		#context['formset'] = QuestionFormset(queryset=Question.objects.none())
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
    