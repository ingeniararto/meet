from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from categories.models import Category

# Create your models here.
class Event(models.Model):
    FREE = "Free"
    ENTRANCE_FEE = "Not free"
    GO_DUTCH = "Go Dutch"
    PAYMENT_CHOICES = (
        (FREE, "Free"),
        (ENTRANCE_FEE, "Not free"),
        (GO_DUTCH, "Go Dutch"),
    )

    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    is_online = models.BooleanField(default=False)
    payment = models.FloatField(default=0)
    payment_type = models.CharField(max_length=8 ,choices=PAYMENT_CHOICES ,default=FREE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE ,null=True ,related_name="events")
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    date = models.DateTimeField(null=True)
    category = models.ForeignKey(Category, on_delete=CASCADE, null=True, related_name="events")

    def get_replies_count(self):
        return Reply.objects.filter(event=self).count()






class Reply(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE , related_name='replies')
    message = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE ,null=True, related_name='replies')
    updated_by = models.ForeignKey(User,on_delete=models.CASCADE ,null=True, related_name='+')