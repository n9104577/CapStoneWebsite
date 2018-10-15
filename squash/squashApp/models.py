from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager 
from django.utils.translation import ugettext_lazy as _
# Create your models here.

# create our own type of user
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
	#date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	is_active = models.BooleanField(_('active'), default=True)
	is_staff = models.BooleanField(_('staff'), default=False)
	
	objects = UserManager()

	# setup model settings
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def get_full_name(self):
		# Returns first_name and last_name with a space inbetween
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		# Returns the short name for the user
		return self.first_name
	def get_preferencetype(self):
		# Returns the short name for the user
		return self.preferencetype
	
	
class Video(models.Model):
	videoId = models.AutoField(primary_key=True)
	name= models.CharField(_('name'), max_length=500)
	player1 = models.ForeignKey('playerData', related_name='player1', on_delete=models.CASCADE)
	player2 = models.ForeignKey('playerData', related_name='player2', on_delete=models.CASCADE)
	noPlayers = models.IntegerField()
	#player1 = models.CharField(_('player1'), max_length=500)
	#player2 = models.CharField(_('player2'), max_length=500)
	videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")

	def __str__(self):
		return self.name + ": " + str(self.videofile)



class videoData(models.Model):
	videoDataId = models.AutoField(primary_key=True)
	videoId = models.ForeignKey('Video', on_delete=models.CASCADE)
	name = models.CharField(_('name'), max_length = 500)	
	processedVideoFile = models.FileField(upload_to='processedVideos/', null=True, verbose_name="")	

	player1HeatMapImage = models.FileField(upload_to='processedImages/', null=True, verbose_name="")
	player1StringLineImage = models.FileField(upload_to='processedImages/', null=True, verbose_name="")
	player1DistanceTravelled = models.FloatField(null=True, blank=True, default=0.0)
	player1TimeInT = models.FloatField(null=True, blank=True, default=0.0)
	player2HeatMapImage = models.FileField(upload_to='processedImages/', null=True, verbose_name="")
	player2StringLineImage = models.FileField(upload_to='processedImages/', null=True, verbose_name="")
	player2DistanceTravelled = models.FloatField(null=True, blank=True, default=0.0)
	player2TimeInT = models.FloatField(null=True, blank=True, default=0.0)
	
	
class playerData(models.Model):
	playerId = models.AutoField(primary_key=True)
	first_name = models.CharField(_('first name'), max_length=30, blank=False)
	last_name = models.CharField(_('last name'), max_length=30, blank=False)
	country = models.CharField(_('country'), max_length=30, blank=False)
	
	def __unicode__(self):
		return '%s %s' % (self.first_name, self.last_name)
		
	def get_name(self):
		return '%s %s' % (self.first_name, self.last_name)








