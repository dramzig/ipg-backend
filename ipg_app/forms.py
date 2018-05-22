from django import forms
from .models import *
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17)
    class Meta:
        model = User
        fields = ('username', 'birth_date', 'phone_number','password1', 'password2', )

class PurchaseOrderForm(forms.Form):
    channel = forms.CharField(max_length=20, required=True)
    class Meta:
        model = PurchaseOrder
        fields = ('channel', )
