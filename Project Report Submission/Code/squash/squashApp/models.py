from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager 
from django.utils.translation import ugettext_lazy as _

# for holding user data
class SquashUser(AbstractBaseUser, PermissionsMixin):
	User_Type = (
		('C', 'Coach'),
		('P', 'Player'),
	)
	
	username = models.CharField(_('username'), max_length=150, unique=True)
	first_name = models.CharField(_('first name'), max_length=30, blank=False)
	last_name = models.CharField(_('last name'), max_length=30, blank=False)
	email = models.EmailField(_('email address'), max_length=254, unique=True)
	usertype = models.CharField(_('user type'),max_length=1, choices=User_Type, blank=True)	
	password = models.CharField(max_length=128)
	is_active = models.BooleanField(_('active'), default=True)
	is_staff = models.BooleanField(_('staff'), default=False)
	
	objects = UserManager()
	
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

# For holding the uploaded video data
class Video(models.Model):
	videoId = models.AutoField(primary_key=True)
	name= models.CharField(_('name'), max_length=500)
	player1 = models.ForeignKey('playerData', related_name='player1', on_delete=models.CASCADE)
	player1Colour = models.CharField(_('playerColour'), max_length= 50);
	player2 = models.ForeignKey('playerData', related_name='player2', on_delete=models.CASCADE)
	player2Colour = models.CharField(_('playerColour'), max_length= 50);
	noPlayers = models.IntegerField()
	videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")
	uploadedBy= models.CharField(_('uploadedBy'), max_length=150)

	def __str__(self):
		return self.name + ": " + str(self.videofile)


# for holding the processed video data
class videoData(models.Model):
	videoDataId = models.AutoField(primary_key=True)
	videoId = models.ForeignKey('Video', on_delete=models.CASCADE)
	name = models.CharField(_('name'), max_length = 500)	
	processedVideoFile = models.FileField(upload_to='processedVideos/', null=True, verbose_name="")	

	player1HeatMapImage = models.FileField(upload_to='processedImages/', null=True, verbose_name="")
	player1StringLineImage = models.FileField(upload_to='processedImages/', null=True, verbose_name="")
	player1DistanceTravelled = models.FloatField(null=True, blank=True, default=0.0)
	player1TimeInT = models.FloatField(null=True, blank=True, default=0.0)
	player1HeatMapVideo = models.FileField(upload_to='processedVideos/', null=True, verbose_name="")
	
	player2HeatMapImage = models.FileField(upload_to='processedImages/', null=True, verbose_name="")
	player2StringLineImage = models.FileField(upload_to='processedImages/', null=True, verbose_name="")
	player2DistanceTravelled = models.FloatField(null=True, blank=True, default=0.0)
	player2TimeInT = models.FloatField(null=True, blank=True, default=0.0)
	player2HeatMapVideo = models.FileField(upload_to='processedVideos/', null=True, verbose_name="")	
	
# for holding player data
class playerData(models.Model):
	playerId = models.AutoField(primary_key=True)
	first_name = models.CharField(_('first name'), max_length=30, blank=False)
	last_name = models.CharField(_('last name'), max_length=30, blank=False)
	country = models.CharField(_('country'), max_length=30, blank=False)
	
	def __unicode__(self):
		return '%s %s' % (self.first_name, self.last_name)
		
	def get_name(self):
		return '%s %s' % (self.first_name, self.last_name)








