"""ce_online_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from online_test import views as test_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-dashboard/',include('online_test.urls')),
    path('user-dashboard/',include('online_test_frontend.urls')),
    path('', include('django.contrib.auth.urls'), {'template_name':"templates/Registration/"}, name='login'),
    path('signup/',test_views.signup, name='signup'),
    # patterns('',
    #            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
    #              {'document_root': settings.MEDIA_ROOT}),
    #           )
    # path('', include('django.contrib.auth.urls'), {'template_name':"templates/registration/"}, name='signup'),
    # path('signup/', views.SignUp.as_view(),{'template_name':"templates/registration/"},name='signup')
]
