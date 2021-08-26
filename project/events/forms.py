from categories.models import Category
from django import forms
from .models import Event, Reply, Attendee
from bootstrap_datepicker_plus import DateTimePickerInput

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
        widget = DateTimePickerInput(format='%Y-%m-%d %H:%M:%S')
    )
    place = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 2, 'placeholder': 'Place'}
        ),     
        required = False,   
        max_length = 4000,
        help_text = 'The max length of the text is 4000.'
    )
    payment_type = forms.ChoiceField(
        required = True,
        choices = Event.PAYMENT_CHOICES
    )
    payment = forms.FloatField(
        initial=0,
        widget = forms.NumberInput(
            attrs = {'rows': 1, 
                'placeholder': 'Fill this area with 0 if the payment type is not \'Not free\' '}
        ),
        help_text = 'In terms of TL.'
    )
    category_name = forms.ChoiceField(
        required = False,
        choices = Category.CATEGORY_CHOICES
    )
    is_online = forms.BooleanField(
        required = False
    )
    max_num_of_attendees = forms.IntegerField(
        required = True
    )
    event_picture = forms.ImageField(
        required=False
    )
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'place', 
            'payment_type','payment', 'category_name', 'is_online', 'max_num_of_attendees', 'event_picture']

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


        