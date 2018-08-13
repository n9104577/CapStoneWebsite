from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

#import forms
from squashApp.forms import RegistrationForm, LoginForm

def index(request):
    return HttpResponse("Hello, world.")
	
	
	
# Homepage view

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
				return render(request, 'squashApp/register.html', {'form': form})

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


def login(request):

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

			return HttpResponseRedirect('smartCityApp/display.html')

		# Else let the user know they entered the wrong details
		else:
			message = '*Incorrect Username or Password'
			return render(request, 'smartCityApp/homepage.html', {'form': form, 'login_message' : message})

	# render the homepage if no form pushed
	return render(request, 'smartCityApp/homepage.html', {'form': form})

