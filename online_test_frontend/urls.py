from django.urls import path

from . import views

app_name = 'online_test_frontend'
urlpatterns = [
	path('<student>/', views.UserDashboardView.as_view(), name='user-dashboard'),
	path('<student>/<exam>', views.TakeTestView.as_view(), name='test'),
	path('hello/test', views.TestView.as_view(), name='test'),
]