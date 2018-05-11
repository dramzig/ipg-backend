from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from .models import *
from simple_history.admin import SimpleHistoryAdmin


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["birth_date", "phone_number"]
    class Meta:
        model = Profile
        fields = "__all__"
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
    list_display = ["id","user", "get_offer","offer_code","created_date", "channel"]
    list_filter = ("offer_code__offer",)
    def get_offer(self, po):
        return po.offer_code.offer
    get_offer.short_description = 'Offer'
    get_offer.admin_order_field = 'offer_code__offer'
    class Meta:
        model = PurchaseOrder

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Catalog, CatalogAdmin)

admin.site.register(SupplyOrder, SupplyOrderAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
#admin.site.register(PurchaseOrder)
admin.site.register(OfferCode, OfferCodeAdmin)
