from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords
from django.core.urlresolvers import reverse


class Country(models.Model):
    name = models.CharField(max_length=20)
    country_code = models.CharField(max_length=4)
    currency = models.CharField(max_length=3)
    sales_tax = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    history = HistoricalRecords()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

class Operator(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    policy = models.TextField()
    term_of_service = models.TextField()
    about = models.TextField()
    history = HistoricalRecords()
    def __str__(self):
        return self.name+"-"+ self.country.name
class Banner(models.Model):
    name = models.CharField(max_length=20)
    order = models.PositiveIntegerField(null=False)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banners/', blank=True)
    target = models.CharField(max_length=255, default='')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, null=False, unique=True )
    country = models.ForeignKey(Country,  on_delete=models.SET_NULL, null=True)
    operator = models.ForeignKey(Operator,  on_delete=models.SET_NULL, null=True)
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
    if not instance.is_staff:
        instance.profile.save()

class Offer(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
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
    in_stock = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    is_new = models.BooleanField(default=False)
    history = HistoricalRecords()
    def __str__(self):
        return self.offer.name
    def get_absolute_url(self):
        return reverse('catalog-detail', args=[str(self.id)])

class PurchaseOrder(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, on_delete=models.PROTECT)
    subtotal = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    taxes_value = models.DecimalField(max_digits=10,decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10,decimal_places=2, default=0)
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

