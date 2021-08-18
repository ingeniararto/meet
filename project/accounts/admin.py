from django.contrib import admin
from .models import Follower, LikedEvent, Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(LikedEvent)
admin.site.register(Follower)