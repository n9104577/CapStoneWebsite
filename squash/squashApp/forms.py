from django import forms
from squashApp.models import SquashUser, Video, videoData, playerData



User_Type = (
		('C', 'Coach'),
		('P', 'Player'),
	)
	

class RegistrationForm(forms.ModelForm):
	first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First Name*'}))
	last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last Name*'}))
	username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username*'}))  
	email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'type':'email', 'placeholder': 'Email*'}))
	password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Password*'}))
	confirm_password= forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password*'}))
	
	
	class Meta:
		model = SquashUser
		fields = ['first_name', 'last_name', 'username', 'usertype',
		'email', 'password']
		




# login form 
class LoginForm(forms.Form):
	username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username*'}))
	password = forms.CharField(max_length=128, widget=forms.PasswordInput(attrs={'placeholder': 'Password*'}))

	class Meta:
		model = SquashUser
		fields = ['username', 'password']



class VideoForm(forms.ModelForm):
	name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Video Title*'}))
	player1 = forms.ModelChoiceField(queryset=playerData.objects.all(), widget=forms.Select(attrs={'class':'drop-down'}), empty_label="Player 1")
	player2 = forms.ModelChoiceField(queryset=playerData.objects.all(), widget=forms.Select(attrs={'class':'drop-down'}), empty_label="Player 2")
	noPlayers = forms.ChoiceField(choices=[(x, x) for x in range(1,3)], widget=forms.Select(attrs={'class':'drop-down'}))
	player1.label_from_instance = lambda obj: "{0} {1}".format(obj.first_name, obj.last_name)
	player2.label_from_instance = lambda obj: "{0} {1}".format(obj.first_name, obj.last_name)
	player1Colour = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Player 1 Colour*'}))
	player2Colour = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Player 2 Colour*'}))
	class Meta:
		model= Video
		fields= ["name", "player1", "player2", "noPlayers", "videofile", "player1Colour", "player2Colour"]

		
		
		
class searchVideoForm(forms.Form):
	searchVideo = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search Video...'}))
	searchPlayer =forms.ModelChoiceField(queryset=playerData.objects.all(), widget=forms.Select(attrs={'class':'drop-down'}),  empty_label="searchPlayer")
	searchPlayer.label_from_instance = lambda obj: "{0} {1}".format(obj.first_name, obj.last_name)
	
	def clean_field(self):
		data = self.cleaned_data['searchPlayer']
		if not data:
			data = 0
		return data

	class Meta:
		model = videoData
		fields=['name', 'player1', 'player2']
	
class searchPlayerForm(forms.Form):
	first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'First Name*'}))
	last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={'placeholder': 'Last Name*'}))
	country = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'placeholder': 'Country*'}))
	
	class Meta:
		model = playerData
		fields=['playerId','first_name','last_name','country']