from django.urls import path

from . import views
from django.conf import settings
from django.contrib.auth.views import login, logout
urlpatterns = [
    
	path('register/', views.register, name='register'),
	path('register/squashApp/login', views.loginView, name='login'),
	path('video', views.video, name='video'),
	path('', views.register, name='register'),
	path('logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='auth_logout')
]