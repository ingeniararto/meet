from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField
# Create your models here.

class Profile(models.Model):
    user = OneToOneField(User ,on_delete=models.CASCADE ,null=True )
    #liked_events
    age = models.IntegerField()
    #gender = models.Choices()