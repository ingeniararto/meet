import datetime
from os import name
from django.core.paginator import Paginator
from django.http.response import HttpResponse
from accounts.models import Follower, LikedEvent, Profile
from django.shortcuts import render, get_object_or_404, redirect
from .models import Attendee, Event, Reply
from .forms import AppreciationForm, NewEventForm, ReplyForm, UpdateEventForm, UpdateReplyForm
from categories.models import Category
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
import json


class Home(View):
    def get(self,request):
        events = Event.objects.all()
        categories = Category.objects.all()
        number_of_events = Event.objects.all().count
        concert = Category.objects.get(id=1)
        food = Category.objects.get(id=2)
        party = Category.objects.get(id=3)
        sport = Category.objects.get(id=4)
        study = Category.objects.get(id=5)
        latest_four_events =Event.objects.filter(date__gt = datetime.date.today()).order_by('-created_by' )[:4]
        past_four_events =Event.objects.filter(date__lte = datetime.date.today()).order_by('-date' )[:4]
        return render(request, 'home.html', {'events': events, 'categories': categories, 
            'number_of_events': number_of_events,'concert' : concert, 'food': food, 'party': party,'sport': sport, 
            'study' : study, 'latest_events': latest_four_events, 'past_events': past_four_events})

class AllEvents(View):
    def get(self,request):
        events = Event.objects.all()
        paginator = Paginator(events, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'all_events.html', {'events': events, 'page_obj': page_obj})



class OneEvent(View):
    def get(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        liked = LikedEvent.objects.filter(event = one_event, liked_by=request.user)
        appreciation_level = []
        attendees = Attendee.objects.filter(event=one_event)
        attended = Attendee.objects.filter(event=one_event, user=request.user)
        for i in range(one_event.get_appreciation_level()):
            appreciation_level.append(i)
        return render(request, 'event.html', {'event': one_event, 'appreciation_level': appreciation_level,
            'attendees': attendees, 'liked': liked, 'attended': attended})
    def post(self, request, pk):
        """user = request.user"""
        one_event = get_object_or_404(Event, pk=pk)
        """if 'Like' in request.POST:
            like = LikedEvent.objects.filter(event= one_event, liked_by=user) 
            if not like: 
                like = LikedEvent.objects.create(liked_by=user, event=one_event)
                like.save()
            else:
                like.delete()
            return redirect('event', pk=pk)
        elif 'Attend' in request.POST:
            attendee = Attendee.objects.filter(event=one_event, user=user) 
            if not attendee : 
                if (one_event.is_there_enough_quota() ):
                    attendee = Attendee.objects.create(event= one_event, user=user)
                    attendee.save()
            else:
                attendee.delete()
            return redirect('event', pk=pk)"""
        if 'Delete' in request.POST:
            Event.objects.filter(pk=one_event.pk).delete()
            return redirect('home')

class NewEvent(LoginRequiredMixin, View):
    def get(self, request):
        form = NewEventForm()
        return render(request, 'new_event.html', {'form': form})
    def post(self, request):
        form = NewEventForm(request.POST, request.FILES )
        if form.is_valid():
            one_event = form.save(commit=False)
            one_event.created_by = request.user
            one_event.category = Category.objects.get(name=one_event.category_name)
            one_event.save()
            return  redirect('all_events')

class UpdateEventView(View):
    def get(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        form = UpdateEventForm(instance=one_event)
        return render(request, 'edit_event.html', {'one_event': one_event, 'form': form})
    def post(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        form = UpdateEventForm(request.POST, instance=one_event)
        if form.is_valid():
            form.save(commit=False)
            if(self.request.user!= one_event.created_by):
                return redirect('event', pk=pk)
            one_event.category = Category.objects.get(name=one_event.category_name)
            one_event.updated_at = datetime.datetime.now()
            one_event.save()
            return redirect('event', pk=pk)

"""class EventUpdate(UpdateView):
    model = Event
    fields = ('name', 'description', 'date', 'place', 'payment_type',
        'payment', 'category_name', 'is_online', 'max_num_of_attendees', 'event_picture')
    template_name = 'edit_event.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'one_event'

    def form_valid(self, form):
        one_event = form.save(commit=False)
        if(self.request.user!= one_event.created_by):
            return redirect('event', pk=one_event.pk)
        one_event.category = Category.objects.get(name=one_event.category_name)
        one_event.updated_at = datetime.datetime.now()
        one_event.save()
        return redirect('event', pk=one_event.pk)"""

class NewReply(LoginRequiredMixin, View):
    def get(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        form = ReplyForm()
        return render(request, 'new_reply.html', {'event': one_event, 
            'form': form})
    def post(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.event = one_event
            reply.created_by = request.user
            reply.save()
            return redirect('event', pk=pk)


class UpdateReplyView(View):
    def get(self, request, pk, id):
        reply = get_object_or_404(Reply, id=id)
        form = UpdateReplyForm(instance = reply)
        return render(request, 'edit_reply.html', {'reply': reply, 'form': form})
    def post(self, request, pk, id):
        reply = get_object_or_404(Reply, id=id)
        form = UpdateReplyForm(request.POST ,instance = reply)
        if form.is_valid():
            form.save(commit=False)
            if(self.request.user!= reply.created_by):
                return redirect('event', pk=reply.event.pk)
            reply.updated_at = datetime.datetime.now()
            reply.save()
            return redirect('event', pk=reply.event.pk)

"""class ReplyUpdate(UpdateView):
    model = Reply
    fields = ('message',)
    template_name = 'edit_reply.html'
    pk_url_kwarg = 'id'
    context_object_name = 'reply'
    def form_valid(self, form):
        reply = form.save(commit=False)
        if(self.request.user!= reply.created_by):
            return redirect('event', pk=reply.event.pk)
        reply.updated_at = datetime.datetime.now()
        reply.save()
        return redirect('event', pk=reply.event.pk)"""


class AppreciationView(LoginRequiredMixin, View):
    def get(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        attendee = get_object_or_404(Attendee, event = one_event, user=request.user )
        form = AppreciationForm()
        return render(request, 'appreciation.html', {'event': one_event, 
            'form': form, 'attendee': attendee})
    def post(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        attendee = get_object_or_404(Attendee, event = one_event, user=request.user)
        form = AppreciationForm(request.POST, instance=attendee)
        print(form)
        print(request.POST)
        if form.is_valid():
            appreciation = form.save(commit=False)
            appreciation.appreciation_level = request.POST['rating3']
            appreciation.appreciated_at = datetime.datetime.now()
            appreciation.save()
            return redirect('event', pk=pk)

class LikeButtonAjax(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        event=get_object_or_404(Event, pk=request.POST['event_pk'])
        likes= LikedEvent.objects.filter(event=event, liked_by=user)
        count= event.get_likes_count()
        if likes:
            is_liked=False
            likes.delete()
            count = count -1
            print ('unliked')
        else:
            is_liked=True
            LikedEvent.objects.create(event=event, liked_by=user)
            count = count +1 
            print ('liked')
        context={'is_liked':is_liked, 'count': count}
        return HttpResponse(json.dumps(context), content_type='application/json')

class AttendButtonAjax(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        event=get_object_or_404(Event, pk=request.POST['event_pk'])
        print (event)
        print('event')
        attendees= Attendee.objects.filter(event=event, user= user)
        print(attendees)
        count= event.get_attendees_count()
        if attendees:
            is_attended=False
            attendees.delete()
            count = count -1
            print ('not attended')
        else:
            is_attended=True
            Attendee.objects.create(event=event, user=user)
            count = count +1 
            print ('attended')
        context={'is_attended':is_attended, 'count': count}
        return HttpResponse(json.dumps(context), content_type='application/json')

class SearchResultsView(View):
    def get(self, request):
        item = self.request.GET.get('item')
        results = Event.objects.filter(name__icontains=item)
        return render(request, 'search_results.html', {'results':results})

class MapView(View):
    def get(self, request):
        return render(request, 'map.html')

    

        




