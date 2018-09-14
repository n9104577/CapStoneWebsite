from django.urls import path

from . import views
from django.conf import settings
from django.contrib.auth.views import login, logout
urlpatterns = [
    
	path('register/', views.register, name='register'),
	path('squashApp/register', views.register, name='register'),
	path('squashApp/login', views.loginView, name='login'),
	path('video', views.video, name='video'),

	path('videoSelection', views.videoSelection, name='videoSelection'),	
	path('videoData/<videoId>', views.videoData, name='videoData'),
	path('playerSelection', views.playerSelection, name='playerSelection'),	
	path('playerData/<playerId>', views.playerData, name='playerData'),
	path('', views.register, name='register'),
	path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='auth_logout')
]