import datetime
from accounts.models import LikedEvent
from django.shortcuts import render, get_object_or_404, redirect
from .models import Attendee, Event, Reply
from .forms import NewEventForm, ReplyForm
from categories.models import Category
from django.views import View
from django.views.generic.edit import UpdateView
from django.http import JsonResponse


# Create your views here.
class Home(View):
    def get(self,request):
        events = Event.objects.all()
        categories = Category.objects.all()
        number_of_events = Event.objects.all().count
        return render(request, 'home.html', {'events': events, 'categories': categories, 
            'number_of_events': number_of_events })

class AllEvents(View):
    def get(self,request):
        events = Event.objects.all()
        return render(request, 'all_events.html', {'events': events})



class OneEvent(View):
    def get(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        return render(request, 'event.html', {'event': one_event, 'flag': False})
    def post(self, request, pk):
        user = request.user
        one_event = get_object_or_404(Event, pk=pk)
        if 'Like' in request.POST:
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
            return redirect('event', pk=pk)
        elif 'Delete' in request.POST:
            Event.objects.filter(pk=one_event.pk).delete()
            return redirect('home')

class NewEvent(View):
    def get(self, request):
        form = NewEventForm()
        return render(request, 'new_event.html', {'form': form})
    def post(self, request):
        form = NewEventForm(request.POST)
        if form.is_valid():
            one_event = form.save(commit=False)
            one_event.created_by = request.user
            one_event.category = Category.objects.get(name=one_event.category_name)
            one_event.save()
            return  redirect('all_events')

class EventUpdate(UpdateView):
    model = Event
    fields = ('name', 'description', 'date', 'place', 'payment_type',
        'payment', 'category_name', 'is_online', 'max_num_of_attendees')
    template_name = 'edit_event.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'one_event'

    def form_valid(self, form):
        one_event = form.save(commit=False)
        one_event.category = Category.objects.get(name=one_event.category_name)
        one_event.updated_at = datetime.datetime.now()
        one_event.save()
        return redirect('event', pk=one_event.pk)

class NewReply(View):
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

class ReplyUpdate(UpdateView):
    model = Reply
    fields = ('message',)
    template_name = 'edit_reply.html'
    pk_url_kwarg = 'id'
    context_object_name = 'reply'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.updated_at = datetime.datetime.now()
        reply.save()
        return redirect('event', pk=reply.event.pk)


class LikeAjax(View):
    def post(self, request):
        data = {'is_liked': True}
        event_pk = request.POST['event_pk']
        one_event = Event.objects.get(pk=event_pk)
        liked = LikedEvent.objects.filter(event=one_event, liked_by=request.user)
        if not liked:
            like = LikedEvent.objects.create(liked_by=request.user, event=one_event)
            like.save()
            data['is_liked'] = True
        else:
            liked.delete()
            data['is_liked'] = False
        return JsonResponse(data)

        




