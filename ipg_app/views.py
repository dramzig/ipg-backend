from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django import http
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, render_to_response
from ipg_app.forms import SignUpForm
from .models import *
from .forms import *
from django.views import generic
from django.core.mail import send_mail
from django.views.generic.edit import CreateView

@login_required
def home(request):
    return render(request, 'catalog.html')

def purchase_error(request):
    return render(request, 'error.html')

def Signup(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('catalog')
    else:
        form = SignUpForm()
    return render(request,'registration/signup.html',{'form':form})


class CatalogListView(generic.ListView):
    model = Catalog
    template_name = 'catalog.html'
    def get_context_data(self, **kwargs):
        #context_object_name = 'catalog_list'
        context = super().get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context
    def get_queryset(self):
        return Catalog.objects.filter(operator__name__icontains='Tigo')

class OfferView(generic.DetailView):
    model= Catalog
    template_name = 'catalog_detail.html'

class PurchaseOrderView(CreateView):
    #form_class=PurchaseOrderForm
    template_name = 'purchaseorder_form.html'
    fields = ['channel', ]
    model = PurchaseOrder
    success_url = 'success'

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(PurchaseOrderView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['user'] = self.request.user.pk
        # etc...
        return initial
    def form_invalid(self, form):
        return http.HttpResponse("form is invalid.. this is just an HttpResponse object")
    #template_name = 'purchaseorder_form.html'


class Success(generic.DetailView):
    model= PurchaseOrder
    template_name = 'success.html'

