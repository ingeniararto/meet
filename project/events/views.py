from django.shortcuts import render
from .models import Event
from django.http import HttpResponse


# Create your views here.

def home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})