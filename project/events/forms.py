from categories.models import Category
from django import forms
from .models import Event, Reply

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
    category = forms.ChoiceField(
        required = False,
        choices = Category.CATEGORY_CHOICES
    )

    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'payment_type','payment','category']

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