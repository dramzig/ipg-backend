from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from ipg_app.forms import SignUpForm
from .models import *
from django.views import generic

@login_required
def home(request):
    return render(request, 'home.html')

def Signup(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request,user)
            return redirect('home')
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
    #    return Catalog.objects()
        return Catalog.objects.filter(operator__name__icontains='Tigo')


# Create your views here.
