from django.shortcuts import render, get_object_or_404
from .models import Event
from django.http import HttpResponse



# Create your views here.

def home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})


def event(request, pk):
    one_event = get_object_or_404(Event, pk=pk)
    return render(request, 'event.html', {'event': one_event})