from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from categories.models import Category
import datetime
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

    name = models.CharField(max_length=70)
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
    max_num_of_attendees = models.IntegerField(default=0)
    event_picture = models.ImageField(upload_to = 'media/events/',null= True , blank = True, editable = True)
    

    def get_replies_count(self):
        return Reply.objects.filter(event=self).count()

    def get_likes_count(self):
        return self.likes.count()

    def get_is_online(self):
        if(self.is_online):
            return 'Online'
        else:
            return 'Face-to-face'
    
    def get_attendees_count(self):
        return self.attendees.count()


    def remaining_quota(self):
        return self.max_num_of_attendees - self.get_attendees_count()

    def is_there_enough_quota(self):
        return (self.remaining_quota() > 0)

    def is_occured(self):
        return  (self.date <= datetime.datetime.now(self.date.tzinfo))

    def get_image(self):
        if not self.event_picture:
            default_path = "static/img/product/no_image.png"
            return default_path
        else:
            return self.event_picture.url

    def get_appreciation_level(self):
        attendees = Attendee.objects.filter(event=self)
        appreciation_level=0
        count = 0
        for attendee in attendees:
            if(attendee.appreciation_level):
                appreciation_level = appreciation_level + int(attendee.appreciation_level)
                count = count + 1
        if(count == 0):
            return 0
        else:
            return int(appreciation_level/count)
    
    def get_appreciation_level_percentage(self):
        attendees = Attendee.objects.filter(event=self)
        appreciation_level=0
        count = 0
        for attendee in attendees:
            if(attendee.appreciation_level):
                appreciation_level = appreciation_level + int(attendee.appreciation_level)
                count = count + 1
        if(count == 0):
            return 0
        else:
            return int((appreciation_level*20)/count)

    def get_place(self):
        list_string = self.place.split(" ")
        string = "+".join(list_string)
        return "https://www.google.com/maps/embed/v1/place?key=AIzaSyD_0BqyEBXLFGblGbei2wEjghxr7nTRt9I&q="+string


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
    appreciation_level = models.CharField(max_length= 1, blank=True, default='0')
    appreciated_at = models.DateTimeField(null=True, default=datetime.datetime.now())