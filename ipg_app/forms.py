from django import forms
from .models import *
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.core.validators import RegexValidator

class SignUpForm(UserCreationForm):
    #country =  forms.ModelChoiceField(queryset = Country.objects.all())
    operator = forms.ModelChoiceField(queryset = Operator.objects.all())
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17)
    #operator = forms.
    class Meta:
        model = User
        fields = ('username','operator','birth_date', 'phone_number','password1', 'password2','email', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Este Email ya está siendo utilizado.')
        return email
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and Profile.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(u'Este telefono ya esta siendo utilizado.')
        return phone_number

class PurchaseOrderForm(forms.Form):
    channel = forms.CharField(max_length=20, required=True)
    catalog = forms.CharField (max_length=20, required=True)
    class Meta:
        model = PurchaseOrder
        fields = ('channel', 'catalog', )

#CART
PRODUCT_QUANTITY_CHOICES = [(i,str(i)) for i in range(1,4)]
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label='Cantidad', choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(label='Actualizar',required=False, initial=False, widget=forms.HiddenInput)



