from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords

#from django.contrib.auth.models import UserAttributeSimilarityValidator

class Profile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Country(models.Model):
    name = models.CharField(max_length=20)
    currency = models.CharField(max_length=3)
    history = HistoricalRecords()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class Operator(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    country = models.ForeignKey(Country)
    history = HistoricalRecords()
    def __str__(self):
        return self.name


class Offer(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    history = HistoricalRecords()
    def __str__(self):
        return self.name


class SupplyOrder(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    history = HistoricalRecords()
    def __str__(self):
        return str(self.created_date)

class OfferCode(models.Model):
    offer = models.ForeignKey(Offer, blank=False, null=False)
    code = models.CharField(max_length=255)
    supply_order = models.ForeignKey(SupplyOrder, blank=False, null=False)
    history = HistoricalRecords()
    def __str__(self):
        return "%s %s" % (self.offer, self.code)

class Catalog(models.Model):
    operator = models.ForeignKey(Operator, blank=True, null=True)
    offer = models.ForeignKey(Offer, blank=True, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    history = HistoricalRecords()
    def __str__(self):
        return str(self.price)
        #return "%s %s %s" % (self.offer.name, self.operator.name, self.price)
