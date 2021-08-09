from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    is_online = models.BooleanField(default=False)
    payment = models.FloatField(default=0)
    #payment_type = models.ChoiceField
    #creater = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='events')
