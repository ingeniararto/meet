from django import forms
from .models import Event, Reply

class NewEventForm(forms.ModelForm):
    name = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 1, 'placeholder': 'Please fill this area.'}
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
            attrs = {'rows': 1, 'placeholder': 'Please give the date'}
        ), 
        help_text = 'format: yyyy-mm-dd hh:mm:ss'
    )
    payment_type = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 1, 'placeholder': 'Please fill this area.'}
        ),
        help_text = 'Free/Not Free/Go Dutch'
    )

    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'payment_type']

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