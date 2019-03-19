from django.urls import path

from . import views

from django.contrib.auth import views as auth_views
from django.conf.urls import url, include


app_name = 'online_test'
urlpatterns = [
	path('', views.DashboardView.as_view(), name='dashboard'),
	path('createtest/',views.CreateTestView.as_view(), name = 'createtest'),
	path('managetests/', views.TestListView.as_view(), name='testmanage'),
	path('managetests/<exam>/<pk>/', views.TestPartView.as_view(), name='testdetail'),
	path('managetests/<exam>/<part>/part', views.TestSectionListView.as_view(), name='sections'),
	path('managetests/<exam>/addnewpart', views.CreatePartView.as_view(), name='createpart'),
	path('managetests/<exam>/<part>/createsinglechoicesection/',views.CreateSectionView.as_view(), name = 'singlechoicecreatesection'),
	path('managetests/<exam>/<part>/createmultiplechoicesection',views.CreateMultipleSectionView.as_view(), name = 'multiplechoicecreatesection'),
	path('managetests/<exam>/<part>/createintegersection',views.CreateIntegerSectionView.as_view(), name = 'integercreatesection'),
	path('managetests/<exam>/<part>/creatematchsection',views.CreateMatchSectionView.as_view(), name = 'matchcreatesection'),
	path('managetests/<exam>/<part>/<section>/<pk>/changesection/',views.UpdateCurrentSection.as_view(), name = 'changesection'),
	path('managetests/<exam>/<part>/<section>/newquestion',views.QuestionChoiceAdd.as_view(), name = 'addnewquestion'),
	path('managetests/<exam>/<part>/<section>/newquestionbatch',views.AddQuestionViewBatch.as_view(), 
		name = 'addnewquestionbatch'),
	path('managetests/<exam>/<part>/<section>/updatesection',views.SectionUpdateView.as_view(), name = 'updatesection'),
	path('managetests/<exam>/<part>/<section>/<question>/',views.AddNewChoices.as_view(), name = 'addnewchoices'),
	path('delete/<exam>/<part>/<section>/<question>/<int:pk>/',views.AuthorDelete.as_view(), name = 'deletequestion'),
	path('delete/<exam>/<part>/<int:pk>/deletesection',views.SectionDelete.as_view(), name='deletesection'),
	path('delete/<slug:slug>/<int:pk>/',views.PartDelete.as_view(), name = 'deletepart'),
	path('delete/<int:pk>/',views.TestDelete.as_view(), name = 'testdelete'),

	#for results
	path('resultslist/', views.ResultListView.as_view(), name='resultlist'),
	path('resultslist/<exam>/', views.ResultDetailView.as_view(), name='resultdetail'),
# <<<<<<< HEAD
	path('login_success/', views.login_success, name='login_success'),
	path('signup/',views.signup, name='signup'),


	
	#path('user/submitselected/',views.get_request_choice, name = 'submitselected'),
	#path('managetests/<slug:slug>/dynamic', views.DynamicChoiceSubmit.as_view(), name='dynamicsubmit'),

	



# =======
	path('resultslist/<exam>/<student>/detail', views.ResultFullDetailView.as_view(), name='resultfulldetail'),
	#path('user/submitselected/',views.get_request_choice, name = 'submitselected'),
	#path('managetests/<slug:slug>/dynamic', views.DynamicChoiceSubmit.as_view(), name='dynamicsubmit'),

# >>>>>>> b6ac48eb66ae46e493034014461d01a7cc71d607
]