from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, RegisterForm
from .models import Profile

# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('registry')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def registry(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            profile = form.save()
            profile.user = request.user
            profile.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registry.html', {'form': form})

def my_account(request,id):
    profile = get_object_or_404(Profile, user=get_object_or_404(User, id=id))
    return render(request, 'my_account.html', {'profile': profile})

