from django.contrib import admin
from squashApp.models import *
# Register your models here.
admin.site.register(SquashUser)
admin.site.register(Video)
admin.site.register(videoData)
admin.site.register(playerData)

