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
from django.shortcuts import redirect
import json
from operator import itemgetter
from django.contrib.auth import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
import sys
sys.path.append("..ce_online_test.settings")

from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.db import transaction


@transaction.atomic
def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            user_obj=User.objects.get(username=user.username) 
            student_form=Student.objects.get(user=user_obj)
            
            
            print(student_form)

            student_form.birth_date=request.POST.get('birth_date')
            # print(student_form.cleaned_data.get('birth_date'))
            student_form.student_username=user.username
            # print(user.username)
            student_form.batch=request.POST.get('batch')
            student_form.address=request.POST.get('address')
            student_form.name=request.POST.get('name')
            # print(student_form.cleaned_data.get('name'))
            student_form.save()            
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('online_test_frontend:user-dashboard', kwargs={'student':user.student_username}))
    else:
        user_form = SignUpForm()
        student_form = StudentForm()
    return render(request, 'online_test/signup.html', {'user_form': user_form, 'student_form':student_form})










def login_success(request):
    """
    Redirects users based on whether they are in the admin group
    to add any user in admin group give him is_staff permission and also add him to admin group
    """
    if request.user.groups.filter(name="admin").exists():
    	print('if')
    	return HttpResponseRedirect(reverse('online_test:dashboard'))
    else:
    	student_username=request.user.username
    	return HttpResponseRedirect(reverse('online_test_frontend:user-dashboard', kwargs={'student':student_username}))









class DashboardView(LoginRequiredMixin,PermissionRequiredMixin, generic.TemplateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
	template_name = 'online_test/dashboard.html'		
		
			
		

	

	
	








class TestListView(LoginRequiredMixin,PermissionRequiredMixin, generic.ListView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
	model = Exam
	template_name = 'online_test/testslist.html'

class TestPartView(LoginRequiredMixin,PermissionRequiredMixin,generic.DetailView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
	model = Exam
	template_name = 'online_test/testpartlist.html'
	slug_field = 'url'

	def get_context_data(self,**kwargs):
		context = super(TestPartView,self).get_context_data(**kwargs)
		# a query that selects all distinct values of part present in sections of that particular exam
		#context['parts'] = Section.objects.order_by('part').distinct('part')
		exam = Exam.objects.get(title=self.kwargs['exam'])
		context['exam'] =exam
		context['pk']=self.kwargs['exam']
		context['parts'] = Part.objects.filter(exam=exam)
		context['questions'] = Question.objects.filter(exam=exam)
		return context

class TestSectionListView(LoginRequiredMixin,PermissionRequiredMixin, generic.ListView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
	model = Section
	template_name = 'online_test/listsections.html'

	def get_queryset(self,**kwargs):
		queryset = super(TestSectionListView, self).get_queryset(**kwargs)
		#part_name = self.kwargs['part']
		test_name = Exam.objects.get(title=self.kwargs['exam'])
		try:
			part_object = Part.objects.get(exam=test_name,name=self.kwargs['part'])
		except:
			part_object=None
		queryset = Section.objects.filter(exam = test_name,part = part_object)
		return queryset
	def get_context_data(self,**kwargs):
		context = super(TestSectionListView,self).get_context_data(**kwargs)
		exam = self.kwargs['exam']
		#part_name = self.kwargs['part']
		test_name = Exam.objects.get(title=exam)
		try:
			part_object = Part.objects.get(exam=test_name,name=self.kwargs['part'])
		except Part.DoesNotExist:
			part_object=None
		context['exam'] = test_name
		context['part'] = part_object
		context['questions'] = Question.objects.filter(exam=test_name,part=part_object)
		return context

class SectionDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
	model = Section

	def get_success_url(self, **kwargs):
		return reverse('online_test:sections',
			kwargs={'exam':self.kwargs['exam'],'part':self.kwargs['part']})

	def get_context_data(self,**kwargs):
		context = super(SectionDelete,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		part_instance = Part.objects.get(exam=exam_instance,name=self.kwargs['part'])
		context['exam'] = exam_instance
		context['part'] = part_instance
		context['pk']=self.kwargs['pk']
		return context	



class CreateTestView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
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

class CreatePartView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
	template_name = 'online_test/newpart.html'
	model = Part
	fields = ('name',)

	def form_valid(self, form,**kwargs):
		form.instance.exam = Exam.objects.get(title=self.kwargs['exam'])
		return super(CreatePartView, self).form_valid(form,**kwargs)

	def get_success_url(self,**kwargs):
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		return reverse('online_test:testdetail',kwargs={'exam':exam_instance, 'pk':exam_instance.id })

	def get_context_data(self,**kwargs):
		context = super(CreatePartView,self).get_context_data(**kwargs)
		exam_instance = Exam.objects.get(title=self.kwargs['exam'])
		context['exam'] = exam_instance
		return context	


class CreateSectionView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
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
		return reverse('online_test:sections',kwargs={'exam':exam_instance,'part':self.kwargs['part'] })

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

class CreateMultipleSectionView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
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
		return reverse('online_test:sections',kwargs={'exam':exam_instance,'part':self.kwargs['part'] })

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

class CreateMatchSectionView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
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
		return reverse('online_test:sections',kwargs={'exam':exam_instance,'part':self.kwargs['part'] })

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

class CreateIntegerSectionView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
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
		return reverse('online_test:sections',kwargs={'exam':exam_instance,'part':self.kwargs['part'] })

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

class AddQuestionViewBatch(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
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

class AddQuestionView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
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


	
class SectionUpdateView(LoginRequiredMixin,PermissionRequiredMixin, generic.TemplateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
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

class AddNewChoices(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
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

class AuthorDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
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

class PartDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
	model = Part

	def get_success_url(self, **kwargs):
		exam = Exam.objects.get(url=self.kwargs['slug'])
		return reverse('online_test:testdetail',
			kwargs={'exam':exam,'pk':exam.id})

	def get_context_data(self,**kwargs):
		context = super(PartDelete,self).get_context_data(**kwargs)
		exam = Exam.objects.get(url=self.kwargs['slug'])
		context['exam'] =exam
		context['parts'] = Part.objects.filter(exam=exam)
		context['sections'] = Section.objects.filter(exam=exam)
		context['questions'] = Question.objects.filter(exam=exam)
		return context 

class TestDelete(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
	model=Exam

	def get_success_url(self, ** kwargs):
		return reverse('online_test:testmanage')

class ResultListView(LoginRequiredMixin,PermissionRequiredMixin, generic.TemplateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
	template_name = 'online_test/testresults.html'

	def get_context_data(self,**kwargs):
		context = super(ResultListView,self).get_context_data(**kwargs)
		tests = Exam.objects.filter(test_completed=True)
		print(tests)
		context['tests'] = tests
		return context

class ResultDetailView(LoginRequiredMixin,PermissionRequiredMixin, generic.TemplateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'
	template_name = 'online_test/singletestresult.html'

	def get_context_data(self,**kwargs):
		context = super(ResultDetailView,self).get_context_data(**kwargs)


		exam = Exam.objects.get(title=self.kwargs['exam'])
		students = Result.objects.filter(test_id=exam)
		context['exam'] = Exam.objects.get(title=self.kwargs['exam'])
		context['students'] = students
		print(students)
		return context

class QuestionChoiceAdd(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
	permission_required = 'user.is_staff'
	login_url = '/accounts/login'
	redirect_field_name = 'redirect'

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
	

class LoginFormMiddleware(object):

    def process_request(self, request):

        # if the top login form has been posted
        if request.method == 'POST' and 'is_top_login_form' in request.POST:

            # validate the form
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():

                # log the user in
                from django.contrib.auth import login
                login(request, form.get_user())

                # if this is the logout page, then redirect to /
                # so we don't get logged out just after logging in
                if '/account/logout/' in request.get_full_path():
                    return HttpResponseRedirect('/')

        else:
            form = AuthenticationForm(request)

        # attach the form to the request so it can be accessed within the templates
        request.login_form = form




