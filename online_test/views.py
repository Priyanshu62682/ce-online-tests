from __future__ import unicode_literals
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy,reverse
from django.views import generic
from .forms import *
from .models import *


class DashboardView(generic.TemplateView):
	#model = Question
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
	form_class = CreateSectionForm
	model = Section

	def get_success_url(self,**kwargs):
		return reverse('online_test:sections',kwargs={'testslug':self.kwargs['exam'],'part':self.kwargs['part'] })

	def get_context_data(self,**kwargs):
		context = super(CreateSectionView,self).get_context_data(**kwargs)
		test_name = self.kwargs['exam']
		part_name = self.kwargs['part']
		test_object = Exam.objects.get(title=test_name)
		part_object = Part.objects.get(exam=test_object, name=part_name)
		context['exam'] = test_object
		context['part'] = part_object
		return context

	def get_form_kwargs(self,**kwargs):
		kwargs = super(CreateSectionView, self).get_form_kwargs()
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		part_instance = Part.objects.get(exam=exam_instance, name=self.kwargs['part'])
		kwargs['part'] = part_instance
		kwargs['exam'] = exam_instance
		return kwargs

class AddQuestionView(CreateView):
	model = Question
	fields = '__all__'
	template_name = 'online_test/newquestion.html'

	def get_success_url(self,**kwargs):
		return reverse('online_test:updatesection',
			kwargs={'exam':self.kwargs['exam'],'part':self.kwargs['part'],'section':self.kwargs['section'] })

	def get_context_data(self,**kwargs):
		context = super(AddQuestionView,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		part_instance = Part.objects.get(exam=exam_instance, name=self.kwargs['part'])
		section_instance = Section.objects.get(exam=exam_instance, part=part_instance,section_type=self.kwargs['section'])
		context['exam'] = exam_instance
		context['part'] = part_instance
		context['section'] = section_instance		
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
	fields = '__all__'
	template_name = 'online_test/newpart.html'


	def get_context_data(self,**kwargs):
		context = super(CreatePartView,self).get_context_data(**kwargs)
		context['slug'] = self.kwargs['testslug']
		return context

	def get_success_url(self,**kwargs):
		return reverse('online_test:testdetail',
			kwargs={'slug':self.kwargs['testslug'] })
