"""ipg_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from ipg_app import views as ipg_views
#Statics images
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', ipg_views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.login, name='logout'),
    url(r'^signup/$', ipg_views.Signup, name='signup'),
    url(r'^catalog/$', ipg_views.CatalogListView.as_view(), name='catalog'),
    url(r'^catalog/(?P<pk>\d+)$', ipg_views.OfferView.as_view(), name='catalog-detail'),
    url(r'^confirmation/(?P<catalog>\d+)$', ipg_views.PurchaseOrderView.as_view(), name='purchase-order'),
    url(r'^success/$', ipg_views.Success, name='success'),
    url(r'^error/$', ipg_views.purchase_error,name='purchase_error'),
    url(r'^cart/$', ipg_views.cart_detail, name='cart_detail'),
    url(r'^cart/add/(?P<product_id>\d+)/$', ipg_views.cart_add, name='cart_add'),
    url(r'^cart/remove/(?P<product_id>\d+)/$', ipg_views.cart_remove, name='cart_remove'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
