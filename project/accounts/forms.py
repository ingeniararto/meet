from collections import namedtuple
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.CharField(
        max_length=254, 
        required=True, 
        widget=forms.EmailInput()
        )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class RegisterForm(forms.ModelForm):
    name = forms.CharField(
        max_length=254, 
        required=True, 
        widget=forms.Textarea(
                attrs = {'rows': 1,}
            )
        )
    surname = forms.CharField(
        max_length=254, 
        required=True, 
        widget=forms.Textarea(
                attrs = {'rows': 1,}
            )
        )
    age = forms.IntegerField(
        widget = forms.NumberInput(
            attrs = {'rows': 1 }
        ),
    )
    gender = forms.ChoiceField(
        required = False,
        choices = Profile.GENDER_CHOICES
    )
    phone_number = forms.IntegerField()
    website = forms.CharField()
    twitter = forms.CharField()
    instagram = forms.CharField()
    facebook = forms.CharField()
    profile_picture = forms.ImageField(
        required=False
    )
    class Meta:
        model = Profile
        fields = [ 'name', 'surname', 'age', 'gender', 'phone_number', 
            'website', 'twitter', 'instagram', 'facebook', 'profile_picture' ]