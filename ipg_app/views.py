from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django import http
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from ipg_app.forms import SignUpForm
from .models import *
from .forms import *
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from .cart import Cart

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

    def get_context_data(self, **kwargs):
        cart_product_form = CartAddProductForm()
        ctx = super(OfferView, self).get_context_data(**kwargs)
        ctx['cart_product_form'] = cart_product_form
        return ctx


class PurchaseOrderView(CreateView):
    #form_class=PurchaseOrderForm
    template_name = 'purchaseorder_form.html'
    fields = ['channel', ]
    model = PurchaseOrder
    success_url = 'success'
    def get_context_data(self, **kwargs):
        ctx = super(PurchaseOrderView, self).get_context_data(**kwargs)
        ctx['catalog'] = "1"
        #self.request.GET.get('catalog')
        return ctx
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(PurchaseOrderView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['user'] = self.request.user.pk
        initial['channel'] = "WW"
        return initial
    def form_invalid(self, form):
        return http.HttpResponse("form is invalid.. this is just an HttpResponse object")
    #template_name = 'purchaseorder_form.html'


class Success(generic.DetailView):
    model= PurchaseOrder
    template_name = 'success.html'

 #CART
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    myProduct = get_object_or_404(Catalog, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(catalog=myProduct, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Catalog, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')
def cart_detail(request):
    cart=Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})
