from django.db import models
# Create your models here.

class Category(models.Model):
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