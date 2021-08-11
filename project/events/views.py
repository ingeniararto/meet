from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, Reply
from .forms import NewEventForm, ReplyForm



# Create your views here.

def home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})


def event(request, pk):
    one_event = get_object_or_404(Event, pk=pk)
    return render(request, 'event.html', {'event': one_event})

def new_reply(request,pk):
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

def new_event(request):
    
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


