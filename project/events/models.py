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

    name = models.CharField(max_length=70, unique=True)
    description = models.CharField(max_length=150)
    is_online = models.BooleanField(default=False)
    payment = models.FloatField(default=0)
    payment_type = models.CharField(max_length=8 ,choices=PAYMENT_CHOICES ,default=FREE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE ,null=True ,related_name="events")
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(null=True)
    date = models.DateTimeField(null=True)
    place = models.CharField(max_length=150, default='Not specified')
    category_name = models.CharField(max_length=7 ,choices=Category.CATEGORY_CHOICES ,default=Category.ELSE)
    category = models.ForeignKey(Category, on_delete=CASCADE, null=True, related_name="events_of_cat")

    def get_replies_count(self):
        return Reply.objects.filter(event=self).count()

    def get_likes_count(self):
        return self.likes.count()

    def get_is_online(self):
        if(self.is_online):
            return 'Online'
        else:
            #return place
            return 'Face-to-face'
    
    def get_attendees_count(self):
        return self.attendees.count()


class Reply(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE , related_name='replies')
    message = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE ,null=True, related_name='replies')


class Attendee(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE , related_name='attendees')
    att_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True, related_name='attended_events')
    DEFAULT = "None"
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    APPRECIATION_CHOICES = (
        (ONE, "1"),
        (TWO, "2"),
        (THREE, "3"),
        (FOUR, "4"),
        (FIVE, "5"),
    )
    appreciation_level = models.CharField(max_length=4 ,choices=APPRECIATION_CHOICES ,default=DEFAULT)