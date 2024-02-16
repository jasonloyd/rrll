from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect


def index(request):
    return render(request, 'index.html', {}) 

def contact(request):
    return HttpResponse("You're at rrll contact.")

def schedule(request):
    return render(request, 'schedule.html', {}) 

def safety(request):
    return render(request, 'safety.html', {}) 