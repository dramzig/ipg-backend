from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ["birth_date", "phone_number"]
    class Meta:
        model = Profile
        fields = "__all__"

#class UserAdmin(admin.ModelAdmin):
#    list_display = ["username", "email"]
#    class Meta:
#        model = User

# Register your models here.
admin.site.register(Profile, ProfileAdmin)
#admin.site.register(User, UserAdmin)
