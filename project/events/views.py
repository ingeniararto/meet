from accounts.models import LikedEvent
from django.shortcuts import render, get_object_or_404, redirect
from .models import Attendee, Event
from .forms import NewEventForm, ReplyForm, AppreciationForm
from categories.models import Category
from django.views import View


# Create your views here.
class Home(View):
    def get(self,request):
        events = Event.objects.all()
        categories = Category.objects.all()
        number_of_events = Event.objects.all().count
        return render(request, 'home.html', {'events': events, 'categories': categories, 'number_of_events': number_of_events })

class AllEvents(View):
    def get(self,request):
        events = Event.objects.all()
        return render(request, 'all_events.html', {'events': events})



class OneEvent(View):
    def get(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        return render(request, 'event.html', {'event': one_event})
    def post(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        user = request.user
        like = LikedEvent.objects.filter(event= one_event, liked_by=user) # in here we filtered the particular post with its id
        if not like: 
            like = LikedEvent.objects.create(liked_by=user, event=one_event)
            like.save()
        return redirect('event',pk=pk)

class NewEvent(View):
    def get(self, request):
        form = NewEventForm()
        return render(request, 'new_event.html', {'form': form})
    def post(self,request):
        form = NewEventForm(request.POST)
        if form.is_valid():
            one_event = form.save(commit=False)
            one_event.created_by = request.user
            one_event.category = Category.objects.get(name=one_event.category_name)
            one_event.save()
            return  redirect('all_events')

class NewReply(View):
    def get(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        form = ReplyForm()
        return render(request, 'new_reply.html', {'event': one_event, 'form': form})
    def post(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.event = one_event
            reply.created_by = request.user
            reply.save()
            return redirect('event', pk=pk)


class Appreciation(View):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        form =AppreciationForm()
        return render(request, 'appreciation.html', {'event': event, 'form': form})
    def post(self, request, pk):
        attendee = get_object_or_404(Attendee, user = request.user)
        form = AppreciationForm(request.POST)
        if form.is_valid():
            level = form.save(commit=False)
            attendee.appreciation_level = level
            attendee.save()
            return redirect('event', pk = pk)
        



