from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, RegisterForm
from .models import Profile
from django.views import View

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
        form = RegisterForm(request.POST)
        if form.is_valid():
            profile = form.save()
            profile.user = request.user
            profile.save()
            return redirect('home')

class Account(View):
    def get(self, request, id):
        profile = get_object_or_404(Profile, user=get_object_or_404(User, id=id))
        liked_events = profile.user.liked_events.all()
        return render(request, 'account.html', {'profile': profile, 'liked_events': liked_events})

