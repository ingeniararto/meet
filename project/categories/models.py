from django.db import models
from django.db.models.fields import TextField
# Create your models here.

class Category(models.Model):
    photo = models.TextField(default=None)
    CONCERT = "Concert"
    FOOD = "Food"
    PARTY = "Party"
    SPORT = "Sport"
    STUDY = "Study"
    ELSE = "Else"
    CATEGORY_CHOICES = (
        (CONCERT, "Concert"),
        (FOOD, "Food"),
        (PARTY, "Party"),
        (SPORT, "Sport"),
        (STUDY, "Study"),
    )
    name = models.CharField(max_length=10 ,choices=CATEGORY_CHOICES ,default=ELSE)

    def get_number_of_events(self):
        return self.events_of_cat.all().count()

    