from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from events.models import Event
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE ,null=True, related_name='profile' )
    name = models.CharField(max_length=22, default="-")
    surname = models.CharField(max_length=22, default="-")
    age = models.IntegerField()
    UNSPECIFIED = "Do not want to specify"
    MALE = "Male"
    FEMALE = "Female"
    GENDER_CHOICES = (
        (UNSPECIFIED, "Do not want to specify"),
        (MALE, "Male"),
        (FEMALE, "Female"),
    )
    gender = models.CharField(max_length=22 ,choices=GENDER_CHOICES ,default=UNSPECIFIED)
    phone_number = models.CharField(default="-",max_length = 13)
    website = models.CharField(default="-",max_length = 100)
    twitter = models.CharField(default="-",max_length = 50)
    instagram = models.CharField(default="-",max_length = 50)
    facebook = models.CharField(default="-",max_length = 50)



class LikedEvent(models.Model):
    event = models.ForeignKey(Event, on_delete= models.CASCADE, null=True, related_name='likes')
    liked_by = models.ForeignKey(User, on_delete=CASCADE, null=True, related_name='liked_events')