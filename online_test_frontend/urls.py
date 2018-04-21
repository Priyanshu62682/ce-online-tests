from django.urls import path

from . import views

app_name = 'online_test_frontend'
urlpatterns = [
	path('<user>/', views.UserDashboardView.as_view(), name='user-dashboard'),
]