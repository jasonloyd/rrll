from django.forms import ModelForm
from django import forms
from django_recaptcha.fields import ReCaptchaField 
from django_recaptcha.widgets import ReCaptchaV3
from .models import VOLUNTEER_ROLES, Volunteer

class SignupForm(ModelForm):
    first_name = forms.TextInput()
    middle_name = forms.TextInput()
    last_name = forms.TextInput()
    email_address = forms.TextInput()
    volunteer_role = forms.CharField(
        max_length=12,
        widget=forms.Select(choices=VOLUNTEER_ROLES),
        initial='UMPIRE',
    )
    abuse_awareness_certificate = forms.FileField()
    captcha = ReCaptchaField(widget=ReCaptchaV3(
        action='signup'
    ))
    
    class Meta:
        model = Volunteer
        fields = ['first_name', 'middle_name', 'last_name', 'email_address', 'volunteer_role', 'abuse_awareness_certificate']
