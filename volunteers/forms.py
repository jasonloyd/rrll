from django.forms import ModelForm
from django import forms
from django_recaptcha.fields import ReCaptchaField 
from django_recaptcha.widgets import ReCaptchaV3
from .models import Volunteer

class SignupForm(ModelForm):
    first_name = forms.TextInput()
    middle_name = forms.TextInput()
    last_name = forms.TextInput()
    email_address = forms.TextInput()
    abuse_awareness_certificate = forms.FileField()
    captcha = ReCaptchaField(widget=ReCaptchaV3(
        action='signup'
    ))
    
    class Meta:
        model = Volunteer
        fields = ['first_name', 'middle_name', 'last_name', 'email_address', 'abuse_awareness_certificate']
        