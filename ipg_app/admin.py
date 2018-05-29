from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django import forms
from .models import *
from simple_history.admin import SimpleHistoryAdmin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["birth_date", "phone_number"]
    class Meta:
        model = Profile
        fields = "__all__"

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, )

class CountryAdmin(SimpleHistoryAdmin):
    list_display = ["name", "currency"]
    class Meta:
        model = Country
        fields = "__all__"
class OperatorAdmin(SimpleHistoryAdmin):
    list_display = ["name", "description", "country"]
    class Meta:
        model = Operator
        fields = "__all__"
class OfferAdmin(SimpleHistoryAdmin):
    list_display = ["name", "description"]
    class Meta:
        model = Offer
class OfferCodeAdmin(SimpleHistoryAdmin):
    list_display = ["id", "offer","code","supply_order","available"]
    list_filter = ('available', "offer")
    class Meta:
        model = OfferCode
class CatalogAdmin(SimpleHistoryAdmin):
    list_display = ["offer","operator","price"]
    list_filter = ('operator',)
    history_list_display = ["status"]
    class Meta:
        model = Catalog
        fields = "__all__"

class OfferCodeInline(admin.TabularInline):
    model = OfferCode
    extra = 0
    fields = ["code","offer"]

class SupplyOrderAdmin(SimpleHistoryAdmin):
    list_display = ["id","created_date", "description"]
    inlines = [OfferCodeInline]
    class Meta:
        model = SupplyOrder

class PurchaseOrderAdmin(SimpleHistoryAdmin):
    list_display = ["id", "user", "created_date", "channel"]
    class Meta:
        model = PurchaseOrder
class PurchaseOrderLineAdmin(SimpleHistoryAdmin):
    list_display = ["purchase_order","id", "offer_id", "offer_name","product_id","currency","price","operator", "country","code","created_date"]
#User
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Catalog, CatalogAdmin)

admin.site.register(SupplyOrder, SupplyOrderAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderLine, PurchaseOrderLineAdmin)
#admin.site.register(PurchaseOrder)
admin.site.register(OfferCode, OfferCodeAdmin)
admin.site.register(Banner)
