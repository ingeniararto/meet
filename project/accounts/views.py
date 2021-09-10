from django.contrib.auth import login as auth_login
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm, RegisterForm, UpdateProfileForm
from .models import Follower, Profile
from django.views import View
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import tzinfo
import json
from django.http.response import HttpResponse, JsonResponse

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
        attended_events = list()
        wlt_attend_events = list()
        upcoming_events = profile.user.events.filter(date__gt = datetime.date.today())
        past_events = profile.user.events.filter(date__lte = datetime.date.today())
        followed = Follower.objects.filter(follower=request.user.profile, followed_profile= profile)
        recommendations = profile.recommendations.all()
        for attended_event in profile.user.attended_events.all() :
            if(attended_event.event.date <= datetime.datetime.now(attended_event.event.date.tzinfo)):
                attended_events.append(attended_event)
        for attended_event in profile.user.attended_events.all() :
            if(attended_event.event.date > datetime.datetime.now(attended_event.event.date.tzinfo)):
                wlt_attend_events.append(attended_event)
        return render(request, 'account.html', {'profile': profile, 'liked_events': liked_events, 
            'attended_events': attended_events,'wlt_attend_events': wlt_attend_events, 'upcoming_events': upcoming_events, 'past_events': past_events, 'followed': followed, 'recommended_events': recommendations})
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

class UpdateProfileView(View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        profile = get_object_or_404(Profile, user=user)
        form = UpdateProfileForm(instance=profile)
        return render(request, 'edit_profile.html', {'profile': profile, 'form':form })
    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        profile = get_object_or_404(Profile, user=user)
        form = UpdateProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save(commit=False)
            if(self.request.user!= profile.user):
                return redirect('account', id=id)
            profile.save()
            return redirect('account', id=id)


"""class ProfileUpdate(UpdateView):
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
        return redirect('account', id=profile.user.id)"""


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
        
class LikedEventsView(LoginRequiredMixin, View):
    def get(self, request):
        liked_events = self.request.user.liked_events.all()
        return render(request, 'liked_events.html', {'liked_events': liked_events})

class WouldLikeToAttendView(LoginRequiredMixin, View):
    def get(self, request):
        wlt_attend_events = self.request.user.attended_events.all()
        attended_events = list()
        for attended_event in wlt_attend_events:
            if(attended_event.event.date > datetime.datetime.now(attended_event.event.date.tzinfo)):
                attended_events.append(attended_event)
        return render(request, 'wlt_attend_events.html', {'attended_events': attended_events})


class FollowButtonAjax(LoginRequiredMixin, View):
    def post(self, request):
        user=request.user
        profile = get_object_or_404(Profile, id= request.POST['profile_id'])
        count = profile.get_num_of_followers()
        follower = Follower.objects.filter(followed_profile = profile, follower=user.profile)
        if not follower: 
            is_followed = True
            follower = Follower.objects.create(follower = request.user.profile, followed_profile = profile)
            count = count + 1
        else: 
            is_followed= False
            follower.delete()
            count = count - 1
        context={'is_followed':is_followed, 'count': count}
        return HttpResponse(json.dumps(context), content_type='application/json')

