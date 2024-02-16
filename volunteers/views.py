from django.shortcuts import get_object_or_404, render, redirect

from django.core.mail import send_mail, EmailMessage

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from django.utils import timezone

from .forms import SignupForm
from .models import Volunteer
from rrll.settings import EMAIL_HOST_USER


def home(request):
    return render(request, 'volunteers/home.html', {'volunteer_list': Volunteer.objects.all()})

def success(request):
    return render(request, 'volunteers/success.html', {})

def volunteer(request, volunteer_id):
    """
    volunteer = cache.get(volunteer_id)
    if volunteer:
        print('cache')
        return render(request, 'volunteers/volunteer.html', {'volunteer': volunteer})

    else:
        print('db')
    """
    volunteer = get_object_or_404(Volunteer, pk=volunteer_id)
    if volunteer is not None:
        # cache.set(volunteer_id, volunteer)
        return render(request, 'volunteers/volunteer.html', {'volunteer': volunteer})

def signup(request):
    error_messages = []
    if request.POST:
        form = SignupForm(request.POST, request.FILES)
        print(request.FILES)
        print(request.POST)
        if form.is_valid():
            form.save()
            subject = "RRLL Volunteer Signup Successful"
            message = request.POST['first_name'] + ", thank you for volunteering! You will receive an email from JDP shortly. Check the volunteers page for volunteer status."
            send_mail(subject, message, EMAIL_HOST_USER, [EMAIL_HOST_USER], True)
            return redirect('volunteers:success')
        else:
            form = SignupForm()
            error_messages.append('Invalid captcha entry, please try again.')
    return render(request, 'volunteers/signup.html', {'form' : SignupForm, 'error_messages': error_messages})
