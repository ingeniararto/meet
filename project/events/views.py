from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Reply
from .forms import NewEventForm, ReplyForm
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

class NewEvent(View):
    def get(self, request):
        if request.method == 'POST':
            form = NewEventForm(request.POST)
            if form.is_valid():
                one_event = form.save(commit=False)
                one_event.created_by = request.user
                one_event.save()
                return redirect('home')
        else:
            form = NewEventForm()
        return render(request, 'new_event.html', {'form': form})

class NewReply(View):
    def get(self, request, pk):
        one_event = get_object_or_404(Event, pk=pk)
        if request.method == 'POST':
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.event = one_event
                reply.created_by = request.user
                reply.save()
                return redirect('event', pk=pk)
        else:
            form = ReplyForm()
        return render(request, 'new_reply.html', {'event': one_event, 'form': form})




