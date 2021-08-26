from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, RegisterForm
from .models import Follower, Profile
from django.views import View
from django.views.generic.edit import UpdateView
import datetime

# Create your views here.

class SignUp(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('registry')

class Registry(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registry.html', {'form': form})
    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save()
            profile.user = request.user
            profile.save()
            return redirect('home')

class Account(View):
    def get(self, request, id):
        profile = get_object_or_404(Profile, user=get_object_or_404(User, id=id))
        liked_events = profile.user.liked_events.all()
        attended_events = profile.user.attended_events.all()
        upcoming_events = profile.user.events.filter(date__gt = datetime.date.today())
        past_events = profile.user.events.filter(date__lte = datetime.date.today())
        return render(request, 'account.html', {'profile': profile, 'liked_events': liked_events, 
            'attended_events': attended_events, 'upcoming_events': upcoming_events, 'past_events': past_events})
    def post(self, request, id):
        profile = get_object_or_404(Profile, user=get_object_or_404(User, id=id))
        if 'follow' in request.POST:
            follower = Follower.objects.filter(follower = request.user.profile, followed_profile = profile) 
            if not follower: 
                follower = Follower.objects.create(follower = request.user.profile, followed_profile = profile)
                follower.save()
            else: 
                follower.delete()
            return redirect('account',id=id)


class ProfileUpdate(UpdateView):
    model = Profile
    fields = ('name', 'surname', 'birthday', 'gender', 'phone_number', 'website', 
        'twitter', 'instagram', 'facebook', 'profile_picture' )
    template_name = 'edit_profile.html'
    pk_url_kwarg = 'id'
    context_object_name = 'profile'

    def form_valid(self, form):
        profile = form.save(commit=False)
        if(self.request.user!= profile.user):
            return redirect('account', id=profile.user.id)
        profile.save()
        return redirect('account', id=profile.user.id)


class FollowersView(View):
    def get(self,request,id):
        profile = get_object_or_404(Profile, user=get_object_or_404(User, id=id))
        followers = profile.followers.all()
        return render(request, 'followers.html', {'profile': profile, 
            'followers': followers })


class ProfilesView(View):
    def get(self, request):
        profiles = Profile.objects.all()
        return render(request, 'profiles.html', {'profiles':profiles})