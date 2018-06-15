from django.urls import path

from . import views

app_name = 'online_test'
urlpatterns = [
	path('', views.DashboardView.as_view(), name='dashboard'),
	path('createtest/',views.CreateTestView.as_view(), name = 'createtest'),
	path('managetests/', views.TestListView.as_view(), name='testmanage'),
	path('managetests/<slug:slug>/', views.TestPartView.as_view(), name='testdetail'),
	path('managetests/<testslug>/<part>/', views.TestSectionListView.as_view(), name='sections'),
	path('managetests/<testslug>/addnewpart', views.CreatePartView.as_view(), name='createpart'),
	path('managetests/<exam>/<part>/createmultiplechoicesection',views.CreateSectionView.as_view(), name = 'singlechoicecreatesection'),
	# path('managetests/<exam>/<part>/createsinglechoicesection',views.CreateMultipleSectionView.as_view(), name = 'multiplechoicecreatesection'),
	# path('managetests/<exam>/<part>/createsinglechoicesection',views.CreateIntegerSectionView.as_view(), name = 'integerchoicecreatesection'),
	# path('managetests/<exam>/<part>/createsinglechoicesection',views.CreateMatchSectionView.as_view(), name = 'matchchoicecreatesection'),
	path('managetests/<exam>/<part>/<section>/newquestion',views.CreateQuestion.as_view(), name = 'addnewquestion'),
	path('managetests/<exam>/<part>/<section>/newquestionbatch',views.AddQuestionViewBatch.as_view(), 
		name = 'addnewquestionbatch'),
	path('managetests/<exam>/<part>/<section>/updatesection',views.SectionUpdateView.as_view(), name = 'updatesection'),
	path('managetests/<exam>/<part>/<section>/<question>/',views.AddNewChoices.as_view(), name = 'addnewchoices'),
	path('delete/<exam>/<part>/<section>/<question>/<int:pk>/',views.AuthorDelete.as_view(), name = 'deletequestion'),
	path('delete/<slug:slug>/<int:pk>/',views.PartDelete.as_view(), name = 'deletepart'),
	path('delete/<int:pk>/',views.TestDelete.as_view(), name = 'testdelete'),

	#for results
	path('resultslist/', views.ResultListView.as_view(), name='resultlist'),
	path('resultslist/<exam>/', views.ResultDetailView.as_view(), name='resultdetail'),
	#path('user/submitselected/',views.get_request_choice, name = 'submitselected'),
	#path('managetests/<slug:slug>/dynamic', views.DynamicChoiceSubmit.as_view(), name='dynamicsubmit'),



]