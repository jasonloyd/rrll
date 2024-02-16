from django.shortcuts import render
from django.http import HttpResponse

from .models import Boardmember

def index(request):
    return render(request, 'boardmembers/index.html', {'boardmember_list': Boardmember.objects.all()})