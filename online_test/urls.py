from django.urls import path,re_path

from . import views

app_name = 'online_test'
urlpatterns = [
	path('', views.DashboardView.as_view(), name='dashboard'),
	path('createtest/',views.CreateTestView.as_view(), name = 'createtest'),
	path('managetests/', views.TestListView.as_view(), name='testmanage'),
	path('managetests/<slug:slug>/', views.TestPartView.as_view(), name='testdetail'),
	path('managetests/<testslug>/<part>/', views.TestSectionListView.as_view(), name='sections'),
#	path('managetests/<testslug>/addnewpart', views.CreatePartView.as_view(), name='createpart'),
	path('managetests/<exam>/<part>/createsection',views.CreateSectionView.as_view(), name = 'createsection'),
	path('managetests/<exam>/<part>/<section>/newquestion',views.AddQuestionView.as_view(), name = 'addnewquestion'),
	path('managetests/<exam>/<part>/<section>/newquestionbatch',views.AddQuestionViewBatch.as_view(), 
		name = 'addnewquestionbatch'),
	path('managetests/<exam>/<part>/<section>/updatesection',views.SectionUpdateView.as_view(), name = 'updatesection'),
	path('managetests/<exam>/<part>/<section>/<question>/',views.AddNewChoices.as_view(), name = 'addnewchoices'),

]