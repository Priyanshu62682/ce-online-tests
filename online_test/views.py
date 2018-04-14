from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from django.views import generic
from django.forms import modelformset_factory
from .forms import *
from .models import *


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
		context['parts'] = Part.objects.filter(exam=self.object)
		context['sections'] = Section.objects.filter(exam=self.object)
		return context

class TestSectionListView(generic.ListView):
	model = Section
	template_name = 'online_test/listsections.html'

	def get_queryset(self,**kwargs):
		queryset = super(TestSectionListView, self).get_queryset(**kwargs)
		test_slug = self.kwargs['testslug']
		part_name = self.kwargs['part']
		test_name = Exam.objects.get(url=test_slug)
		part_object = Part.objects.get(exam=test_name,name=part_name)
		queryset = Section.objects.filter(exam = test_name,part = part_object)
		return queryset
	def get_context_data(self,**kwargs):
		context = super(TestSectionListView,self).get_context_data(**kwargs)
		test_slug = self.kwargs['testslug']
		part_name = self.kwargs['part']
		test_name = Exam.objects.get(url=test_slug)
		part_object = Part.objects.get(exam=test_name,name=part_name)
		context['exam'] = test_name
		context['part'] = part_object
		return context


class CreateTestView(CreateView):
	model = Exam
	fields = '__all__'
	template_name = 'online_test/createtest.html'
		

class CreateSectionView(CreateView):
	template_name = 'online_test/createnewsection.html'
	model = Section
	fields = ('section_type','positive_marks','negative_marks','section_instructions',)

	def form_valid(self, form,**kwargs):
		form.instance.exam = Exam.objects.get(title=self.kwargs['exam'])
		form.instance.part = Part.objects.get(exam=form.instance.exam, name=self.kwargs['part'])
		return super(CreateSectionView, self).form_valid(form,**kwargs)

	def get_success_url(self,**kwargs):
		return reverse('online_test:sections',kwargs={'testslug':self.kwargs['exam'],'part':self.kwargs['part'] })

	def get_context_data(self,**kwargs):
		context = super(CreateSectionView,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		part_instance = Part.objects.get(exam=exam_instance, name=self.kwargs['part'])
		context['exam'] = exam_instance
		context['part'] = part_instance
		return context

class AddQuestionView(CreateView):
	model = Question
	fields = ('content','figure',)
	template_name = 'online_test/newquestion.html'
	# def get_initial(self,**kwargs):
	# 	exam_instance = Exam.objects.get(title=self.kwargs['exam'])
	# 	part_instance = Part.objects.get(exam=exam_instance, name=self.kwargs['part'])
	# 	section_instance = Section.objects.get(exam=exam_instance, part=part_instance,section_type=self.kwargs['section'])
	# 	return {'exam': exam_instance,
	# 	'part': part_instance,
	# 	'section':section_instance}

	def form_valid(self, form,**kwargs):
		form.instance.exam = Exam.objects.get(title=self.kwargs['exam'])
		form.instance.part = Part.objects.get(exam=form.instance.exam, name=self.kwargs['part'])
		form.instance.section = Section.objects.get(
			exam=form.instance.exam, part=form.instance.part,section_type=self.kwargs['section'])	
		return super(AddQuestionView, self).form_valid(form,**kwargs)

	def get_success_url(self,**kwargs):
		return reverse('online_test:updatesection',
			kwargs={'exam':self.kwargs['exam'],'part':self.kwargs['part'],'section':self.kwargs['section'] })

	def get_context_data(self,**kwargs):
		context = super(AddQuestionView,self).get_context_data(**kwargs)
		context['exam'] = self.kwargs['exam']
		context['part'] = self.kwargs['part']
		context['section'] = self.kwargs['section']		
		return context
	
class SectionUpdateView(generic.TemplateView):
	model = Section
	template_name = 'online_test/sectiondetail.html'

	def get_context_data(self,**kwargs):
		context = super(SectionUpdateView,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		part_instance = Part.objects.get(exam=exam_instance, name=self.kwargs['part'])
		section_instance = Section.objects.get(exam=exam_instance, part=part_instance,section_type=self.kwargs['section'])
		context['exam'] = exam_instance
		context['part'] = part_instance
		context['section'] = section_instance		
		context['questions'] = Question.objects.filter(
			exam=exam_instance,
			part=part_instance,
			section=section_instance)
		return context

class CreatePartView(CreateView):
	model = Part
	fields = ('name',)
	template_name = 'online_test/newpart.html'

	def form_valid(self, form,**kwargs):
		form.instance.exam = Exam.objects.get(url=self.kwargs['testslug'])
		return super(CreatePartView, self).form_valid(form,**kwargs)

	def get_context_data(self,**kwargs):
		context = super(CreatePartView,self).get_context_data(**kwargs)
		context['slug'] = self.kwargs['testslug']
		return context

	def get_success_url(self,**kwargs):
		return reverse('online_test:testdetail',
			kwargs={'slug':self.kwargs['testslug'] })

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
		part_instance = Part.objects.get(exam=exam_instance, name=self.kwargs['part'])
		section_instance = Section.objects.get(exam=exam_instance, part=part_instance,section_type=self.kwargs['section'])
		question_instance = Question.objects.get(id=self.kwargs['question'])
		context['exam'] = exam_instance
		context['part'] = part_instance
		context['section'] = section_instance	
		context['question'] = question_instance
		return context