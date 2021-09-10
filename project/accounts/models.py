from operator import length_hint
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from numpy import sqrt
from events.models import Attendee, Event
import datetime
from events.kmeans import k_means_event
from queue import PriorityQueue
# Create your models here.

def find_dist(center_1, center_2):
       return sqrt((center_1[0]-center_2[0])**2 + (center_1[1] - center_2[1])**2 + (center_1[2]-center_2[2])**2)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
        null=True, related_name='profile' )
    name = models.CharField(max_length=22, default="-")
    surname = models.CharField(max_length=22, default="-")
    birthday = models.DateField(null=True)
    UNSPECIFIED = "Do not want to specify"
    MALE = "Male"
    FEMALE = "Female"
    GENDER_CHOICES = (
        (UNSPECIFIED, "Do not want to specify"),
        (MALE, "Male"),
        (FEMALE, "Female"),
    )
    gender = models.CharField(max_length=22, choices=GENDER_CHOICES,
        default=UNSPECIFIED)
    phone_number = models.CharField(default="-", max_length = 13)
    website = models.CharField(default="-", max_length = 100)
    twitter = models.CharField(default="-", max_length = 50)
    instagram = models.CharField(default="-", max_length = 50)
    facebook = models.CharField(default="-", max_length = 50)
    profile_picture = models.ImageField(upload_to = 'static/uploads/', default= None, blank = True, editable = True)
    recommendations = models.ManyToManyField(Event, null=True, related_name='recommended_to_profile', )

    def get_num_of_followers(self):
        return self.followers.all().count()

    def get_image(self):
        if(self.profile_picture):
            print('success')
            return self.profile_picture.url
        else:
            print('fail')
            if(self.gender=='Male'):
                print('Male')
                return "https://bootdey.com/img/Content/avatar/avatar2.png"
            elif (self.gender == 'Female'):
                print('Female')
                return "https://bootdey.com/img/Content/avatar/avatar3.png"
            else:
                print('Else')
                return "https://www.yesilist.com/wp-content/uploads/2016/03/no-user-image.gif"



    def get_recommendations(self):
        self.recommendations.clear()
        user= self.user
        attended_events = Attendee.objects.filter(user=user)
        if( not attended_events):
            return self.recommendations
        followers= self.followed_profiles.all()
        clusters, kmeans, cluster_labels = k_means_event(user)
        centers = kmeans.cluster_centers_
        heap = PriorityQueue(20)
        print("success")
        for follower_ in followers:
            follower = follower_.followed_profile
            clusters_follower, kmeans_follower, cluster_labels_follower = k_means_event(follower.user)
            if(clusters_follower==[] and kmeans_follower==[] and cluster_labels_follower==[]):
                continue
            centers_follower = kmeans_follower.cluster_centers_
            for center in centers:
                counter = 0
                for center_follower in centers_follower:
                    dist = find_dist(center, center_follower)
                    heap.put((dist, cluster_labels_follower[counter]))
                    counter = counter +1
        i=0
        while i<4 and not heap.empty() :
            array= heap.get()[1]
            j=0
            while i<4 and j< len(array):
                event = Event.objects.get(pk=array[j])
                attendee = Attendee.objects.filter(user=user, event=event)
                if( not attendee):
                    self.recommendations.add(event)
                    i = i+1
                    j = j+1
        
        return self.recommendations


                        





class LikedEvent(models.Model):
    event = models.ForeignKey(Event, on_delete= models.CASCADE, 
        null=True, related_name='likes')
    liked_by = models.ForeignKey(User, on_delete=CASCADE, 
        null=True, related_name='liked_events')


class Follower(models.Model):
    follower = models.ForeignKey(Profile, on_delete=CASCADE, 
        null=True, related_name= 'followed_profiles')
    followed_profile = models.ForeignKey(Profile, on_delete=CASCADE, 
        null=True, related_name='followers')