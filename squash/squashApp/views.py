from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
# Create your views here.

#import forms
from squashApp.forms import RegistrationForm, LoginForm


# Import Password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
#from django.contrib.auth.decorators import login_required

# This file renders all the pages and does most the form proccessing

# Import relevant functions, models, forms, ect

# rendering
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

# security 
from django.template.context_processors import csrf
from django.template.loader import get_template
from django.template import RequestContext
from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
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
from squashApp.models import SquashUser

from squashApp import models
from django.conf.urls import url
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
	
	
# User RegistrationForm
def register(request):
	form = RegistrationForm()
	# process the Register Form"
	if 'Register' in request.POST:
		form = RegistrationForm(request.POST)
		print('register in post')

		# make sure form is valid
		if form.is_valid():
			print("form valid")
			# clean the form
			form.clean()

			# check passwords match
			if form.cleaned_data['password'] == form.cleaned_data['password_confirm']:
				register = form.save(commit=False)

				# hash the password
				register.password = make_password(form.cleaned_data['password'])
				register.status=1

				# register the user with hashed password
				register.save()

				# return to the homepage so the user can login, set form1 to form so the users username is already entered.
				# and they know it was successful
				return HttpResponseRedirect('squashApp/login', {'form': form})
				return render(request, 'squashApp/login.html', {'form': form})
				
			# else return a message saying the passwords dont match
			elif form.data['password'] != form.data['password_confirm']:
				message = '*Passwords do not match!'
				context = {
					'form': form,					
					'register_password_message' : message,
				}
				return render(request, 'squashApp/register.html', context)

			# shouldnt reach here password either match or dont match
			else:
				form = RegistrationForm()
				
	return render(request, 'squashApp/register.html', {'form': form})

# User Login
def loginView(request):

	# Preset each form for first time loading of the homepage

	form = LoginForm()

	# process the Login Form"
	if 'Login' in request.POST:

		# Get the username and password entered
		username = request.POST['username']
		password = request.POST['password']

		# Check them against the database
		user = authenticate(username=username, password=password)

		# if user and pass match, login and redirect to the display page
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/video')
			return render(request, 'squashApp/homepage.html')
			return HttpResponseRedirect('squashApp/homepage.html')

		# Else let the user know they entered the wrong details
		else:
			message = '*Incorrect Username or Password'
			return render(request, 'squashApp/login.html', {'form': form, 'login_message' : message})

	# render the homepage if no form pushed
	return render(request, 'squashApp/login.html', {'form': form})

@login_required	
def video(request):
	return render(request, 'squashApp/homepage.html')

	
@login_required
def logout(request):
	db.connections.close_all()
	logout(request)
