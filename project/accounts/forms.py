from collections import namedtuple
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from .models import Profile
from bootstrap_datepicker_plus import DatePickerInput

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
    birthday = forms.DateField(
        widget = DatePickerInput(format='%Y-%m-%d')
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
        fields = [ 'name', 'surname', 'birthday', 'gender', 'phone_number', 
            'website', 'twitter', 'instagram', 'facebook', 'profile_picture' ]


class UpdateProfileForm(forms.ModelForm):
    birthday = forms.DateField(
        widget = DatePickerInput(format='%Y-%m-%d')
    )
    class Meta:
        model = Profile
        fields = [ 'name', 'surname', 'birthday', 'gender', 'phone_number', 
            'website', 'twitter', 'instagram', 'facebook', 'profile_picture' ]