

#import forms
from squashApp.forms import RegistrationForm, LoginForm, searchVideoForm, searchPlayerForm


# Import Password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

# Import relevant functions, models, forms, ect

# rendering
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

# security 
from django.template.context_processors import csrf
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib import auth, messages

from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.views.generic import *
from django import db, template

# admin
from django.contrib.admin import AdminSite

# users, forms and models
from squashApp.models import SquashUser, playerData

from squashApp import models
from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from itertools import chain	
from itertools import groupby
	
# for video upload
from .models import Video
from .forms import VideoForm
	


# import tracking script	
from squashApp.SquashTracking import main


# User RegistrationForm
def register(request):
	form = RegistrationForm()
	# process the Register Form"
	if 'registerForm' in request.POST:
		form = RegistrationForm(request.POST)

	
		if form.is_valid():
			form.clean()
			
			# if passwords match
			if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
				register = form.save(commit=False)
				register.password = make_password(form.cleaned_data['password'])
				register.status=1
				register.usertype = 'P'
				register.save()
				return HttpResponseRedirect('squashApp/login', {'form': form})
			# if they dont
			else:
				message = 'Password didnt match*'
				context = {
					'form': form,					
					'password_error' : message,
				}
				return render(request, 'squashApp/register.html', context)
	return render(request, 'squashApp/register.html', {'form': form})

# User Login
def loginView(request):
	form = LoginForm()

	# check form
	if 'loginForm' in request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		
		# if user can login then login
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/uploadVideo')
		else: # else return a message
			message = 'UserName or Password wrong*'
			return render(request, 'squashApp/login.html', {'form': form, 'login_error' : message})

	return render(request, 'squashApp/login.html', {'form': form})

	
# For uploading the video   
@login_required	
def uploadVideo(request):
	
	# get the form and check if its valid
	form= VideoForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		
		# clean and set the user as a player by default then save
		form.clean()
		editform = form.save(commit=False)
		user= request.user.username
		editform.uploadedBy = user
		form.save()
		
		# get the uploaded video and process it 
		videoObject= Video.objects.last()
		videofile= videoObject.videofile
		videoName = videoObject.name
		
		noPlayers = videoObject.noPlayers
		main(videofile.url[1:], videoName, videoObject, noPlayers) # main processing script
		videoId = videoObject.videoId
		
		# redirect to the output page
		redirect = "/videoData/" + str(videoId)
		return HttpResponseRedirect(redirect)
	
	
	context= {'form': form}		
	return render(request, 'squashApp/uploadVideo.html', context)
	
	

# for selecting a video
@login_required	
def videoSelection(request):
	# get and set variables/constants
	form = searchVideoForm()
	showSearch = False
	videoList = models.Video.objects.all()
	reversedList=list(reversed(videoList))
	
	# if there is a search query 
	# retrieve the required videos
	if 'search' in request.POST:
		searchVideo = request.POST['searchVideo']
		searchPlayer = request.POST['searchPlayer']		
		player1List = models.Video.objects.filter(name__icontains=searchVideo, player1=searchPlayer).all()
		player2List = models.Video.objects.filter(name__icontains=searchVideo, player2=searchPlayer).all()
		List = list(chain(player1List, player2List))
		videoList = list(dict.fromkeys(List))
		reversedList=list(reversed(videoList))		
		showSearch = True
	
	# else just return all videos
	if(len(videoList) < 1):
		videoList = models.Video.objects.all()
		reversedList=list(reversed(videoList))
		
		showSearch = False
	
	# set the context
	context = {
		'username': request.user.username,
		'videoList': videoList,
		'reversedList':reversedList,
		'form': form,
		'showSearch': showSearch
	}
	
	return render(request, 'squashApp/videoSelection.html', context)		

	
# show the video data
@login_required		
def videoData(request, videoId):
	video = models.videoData.objects.get(videoId_id=videoId)
	parentvideo = models.Video.objects.get(videoId=videoId)
	player1 = models.playerData.objects.get(playerId=parentvideo.player1.playerId)
	player2 = models.playerData.objects.get(playerId=parentvideo.player2.playerId)

	context = {'video': video, 'player1': player1, 'player2': player2, 'parentvideo': parentvideo}
	return render(request, 'squashApp/videoData.html', context)

	
#show a list of players
@login_required		
def playerSelection(request):
	form = searchPlayerForm()
	showSearch = False
	playerList = models.playerData.objects.all()
	
	# if there is a search
	if 'search' in request.POST:		
		first = request.POST['first_name']
		last = request.POST['last_name']
		p_country = request.POST['country']
		
		List = models.playerData.objects.filter(first_name__icontains=first, last_name__icontains=last, country__icontains=p_country).all()	
		playerList = list(dict.fromkeys(List))
		showSearch = True
	
	# if no seach
	if(len(playerList) < 1):
		playerList = models.playerData.objects.all()
		showSearch = False
	
	# context
	context = {
		'username': request.user.username,
		'playerList': playerList,
		'form': form,
		'showSearch': showSearch
	}
	
	return render(request, 'squashApp/playerSelection.html', context)


	
# show player data
@login_required		
def playerData(request, playerId):
	player = models.playerData.objects.get(playerId=playerId)
	videoList = models.Video.objects.all()
	context= {'player': player, 'videoList' : videoList}

	return render(request, 'squashApp/playerData.html', context)

# help page
@login_required		
def help(request):	
	return render(request, 'squashApp/help.html')
	
	
# close db_connection on logout
@login_required
def logout(request):
	db.connections.close_all()
	logout(request)




