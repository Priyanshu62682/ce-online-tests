from django.urls import path

from . import views

app_name = 'online_test_frontend'
urlpatterns = [
	path('<student>/', views.UserDashboardView.as_view(), name='user-dashboard'),
	path('<student>/<exam>/', views.TakeTestView.as_view(), name='test'),
	#path('hello/test', views.TestView.as_view(), name='test'),
	path('user/submitselected',views.get_request_choice, name = 'submitselected'),
	path('<student>/<exam>/testinfo/',views.UserTestInfo.as_view(), name = 'usertestinfo'),
	path('<student>/<exam>/confirm_registration/',views.SubscribeTest.as_view(), name = 'subscribetest'),
	path('<student>/<exam_id>/endtest/', views.Thank_view, name='thankyou'),
]