from django.shortcuts import render, get_object_or_404
from .models import Category
from events.models import Event
# Create your views here.

def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories': categories})

def category(request, id):
    category = get_object_or_404(Category, id = id)
    events = Event.objects.filter(category=category)
    return render(request, 'category.html', {'events': events, 'category': category})