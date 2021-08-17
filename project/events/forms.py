from django.db.models import fields
from accounts.models import LikedEvent
from categories.models import Category
from django import forms
from .models import Event, Reply, Attendee

class NewEventForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 1, 'placeholder': 'The name of the event'}
        ),        
    )
    description = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 5, 'placeholder': 'What is on your mind?'}
        ),        
        max_length = 4000,
        help_text = 'The max length of the text is 4000.'
    )
    date = forms.DateTimeField(
        widget = forms.Textarea(
            attrs = {'rows': 1, 'placeholder': 'Please give the date of event'}
        ), 
        help_text = 'format: yyyy-mm-dd hh:mm:ss'
    )
    place = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 5, 'placeholder': 'Place'}
        ),        
        max_length = 4000,
        help_text = 'The max length of the text is 4000.'
    )
    payment_type = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 1, 'placeholder': 'Please indicate the payment type'}
        ),
        help_text = 'Free/Not free/Go Dutch'
    )
    payment = forms.FloatField(
        widget = forms.NumberInput(
            attrs = {'rows': 1, 'placeholder': 'Fill this area if the payment type is \'Not free\' '}
        ),
        help_text = 'In terms of TL.'
    )
    category_name = forms.ChoiceField(
        required = False,
        choices = Category.CATEGORY_CHOICES
    )
    is_online = forms.BooleanField(
        required = True
    )
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'place', 'payment_type','payment', 'category_name', 'is_online']

class ReplyForm(forms.ModelForm):
    message = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 5, 'placeholder': 'What is on your mind?'}
        ),        
        max_length = 4000,
        help_text = 'The max length of the text is 4000.'
    )
    class Meta:
        model = Reply
        fields = ['message', ]


class AppreciationForm(forms.ModelForm):
    appreciation_level = forms.ChoiceField(
        required = False,
        choices = Attendee.APPRECIATION_CHOICES
    )

    class Meta:
        model = Attendee
        fields = ['appreciation_level', ]


        