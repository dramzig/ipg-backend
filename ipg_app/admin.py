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

class CatalogAdmin(SimpleHistoryAdmin):
    list_display = ["offer","operator","price"]
    list_filter = ('operator',)
    history_list_display = ["status"]
    class Meta:
        model = Catalog
        fields = "__all__"

class OfferCodeInline(admin.StackedInline):
    model = OfferCode
    extra = 0
    fields = ["offer","code"]
    #readonly_fields = ["offer"]

class SupplyOrderAdmin(SimpleHistoryAdmin):
    list_display = ["id","created_date", "description"]
    inlines = [OfferCodeInline]
    class Meta:
        model = SupplyOrder

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Catalog, CatalogAdmin)

admin.site.register(SupplyOrder, SupplyOrderAdmin)

#admin.site.register(User, UserAdmin)
