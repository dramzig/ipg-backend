from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from django.core.urlresolvers import reverse

#from django.contrib.auth.models import UserAttributeSimilarityValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=False, unique=True )
    def clean(self):
        cleaned_data = super(Profile, self).clean()
        return cleaned_data

    def save(self, *args, **kwargs):
        self.validate_unique()
        super(Profile, self).save(*args, **kwargs)

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
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.name


class SupplyOrder(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    history = HistoricalRecords()
    def __str__(self):
        return str(self.id)

class OfferCode(models.Model):
    code = models.CharField(max_length=255)
    offer = models.ForeignKey(Offer, blank=True, null=True)
    supply_order = models.ForeignKey(SupplyOrder, blank=False, null=False)
    available = models.BooleanField(default=True)
    #purchase_order = models.ForeignKey(PurchaseOrder, blank=True, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.code

class Catalog(models.Model):
    operator = models.ForeignKey(Operator, blank=True, null=True)
    offer = models.ForeignKey(Offer, blank=True, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    history = HistoricalRecords()
    def __str__(self):
        return self.offer.name
    def get_absolute_url(self):
        return reverse('catalog-detail', args=[str(self.id)])

class PurchaseOrder(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.PROTECT)
    #catalog = models.ForeignKey(Catalog, blank=False, null=True, on_delete=models.PROTECT)
    #offer_code = models.ForeignKey(OfferCode, blank=True, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True)
    channel = models.CharField(max_length=20)
    history = HistoricalRecords()
    def __str__(self):
        return str(self.id)
class PurchaseOrderLine(models.Model):
    offer_id = models.PositiveIntegerField(null=False)
    offer_name = models.CharField(max_length=50, null=False)
    product_id = models.PositiveIntegerField(null=False)
    currency = models.CharField(max_length=3)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    operator = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    code = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    purchase_order = models.ForeignKey(PurchaseOrder, blank=False, null=False)
    history = HistoricalRecords()
    def __str__(self):
        return str(self.id)

