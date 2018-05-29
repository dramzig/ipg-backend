from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django import http
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from .models import *
from .forms import *
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.generic.edit import CreateView
from .cart import Cart
from django.db import transaction
from django.urls import reverse_lazy

import logging
logger = logging.getLogger('__name__')


def load_operators(request):
    country_id = request.GET.get('country')
    operators = Operator.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'registration/operator_dropdown_list_options.html', {'operators': operators})

@login_required
def home(request):
    return render(request, 'catalog.html')

def purchase_error(request):
    return render(request, 'error.html')


@transaction.atomic
def Signup(request):
    if request.method == 'POST':
        form =SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.country = form.cleaned_data.get('country')
            user.profile.operator = form.cleaned_data.get('operator')
            if Profile.objects.filter(phone_number=user.profile.phone_number).count() > 0:
                raise ValidationError('This display name is already in use.')
            user.save()
            logger.warning("request.POST: " + str(request.POST))
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
        context['banners'] = Banner.objects.filter(operator=self.request.user.profile.operator)
        context['some_data'] = 'This is just some data'
        return context
    def get_queryset(self):
        return Catalog.objects.filter(operator=self.request.user.profile.operator)

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
@login_required
def cart_add(request, product_id):
    cart = Cart(request)
    myProduct = get_object_or_404(Catalog, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(catalog=myProduct, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart_detail')
@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Catalog, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart=Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})


@login_required
@transaction.atomic
def cart_checkout(request):
    cart = Cart(request)
    logger.warning("Comenzando")
    po = PurchaseOrder(user =  request.user, channel = 'WEB')
    po.save()
    logger.warning("PO ID: "+str(po.id))
    for item in cart:
        for quantityIterator in range (0,item['quantity']):
            purchaseOrderLine = PurchaseOrderLine(
                offer_id=item['product'].offer.id,
                offer_name=item['product'].offer.name,
                product_id=item['product'].id,
                currency = item['product'].operator.country.currency,
                price = item['product'].price,
                operator = item['product'].operator.name,
                country = item['product'].operator.country.name,
                code = "11111111",
                purchase_order = po
            )
            logger.warning("quantityIterator "+str(quantityIterator)+": PO:"+str(purchaseOrderLine))
            purchaseOrderLine.save()
    cart.clear()
    return render(request, 'cart/checkout.html', {'cart': cart})
    #return render(request, 'cart/checkout.html', {'cart': cart})


#offer_id = models.PositiveIntegerField(null=False)
#offer_name = models.CharField(max_length=50, null=False)
#product_id = models.PositiveIntegerField(null=False)
#price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#operator = models.CharField(max_length=20)
#country = models.CharField(max_length=20)
#code = models.CharField(max_length=255)
#created_date = models.DateTimeField(auto_now_add=True)
#purchase_order = models.ForeignKey(PurchaseOrder, blank=False, null=False)
