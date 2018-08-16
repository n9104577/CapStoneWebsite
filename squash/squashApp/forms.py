from django import forms
from squashApp.models import SquashUser










User_Type = (
		('C', 'Coach'),
		('P', 'Player'),
	)
	
# Used for registering a user
class RegistrationForm(forms.ModelForm):
	first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First Name*'}))
	last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last Name*'}))
	username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username*'}))
	usertype = forms.ChoiceField(choices=User_Type, required=True, widget=forms.Select(attrs={'class':'drop-down'}))                                  
	email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'type':'email', 'placeholder': 'Email*'}))
	password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Password*'}))
	password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password*'}))
	
	# assign the form a model to save to and which fields to save
	class Meta:
		model = SquashUser
		fields = ['first_name', 'last_name', 'username', 'usertype',
		'email', 'password'] # Or list '__all__'
		#widget = {
		#'usertype': forms.Select(attrs={'style': 'background-color: blue'}),
		#}
		#widgets = {
		#'password': forms.PasswordInput(),
		#}
		#exclude = ['title']




# login form 
class LoginForm(forms.Form):
	username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username*'}))
	password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Password*'}))

	class Meta:
		model = SquashUser
		fields = ['username', 'password']
		
		
		
		
		
		
