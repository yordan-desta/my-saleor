import uuid as uuid
from django.db import models
from django_countries.fields import CountryField

from ...shipping import models as ship

ACTIVE = 'A'
PENDING = 'P'
SUSPENDED = 'S'
CLOSED = 'C'
MERCHANT_ACCOUNT_STATUS = ((PENDING, "Pending"), (ACTIVE, "Active"), (SUSPENDED, "Suspended"), (CLOSED, "Closed"))

class Merchant(models.Model):
    # merchant_type = models.ForeignKey(MerchantType, on_delete=models.ProtectedError, to_field="uuid")
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    shipping_method = models.ManyToManyField(ship.ShippingMethod, related_name="merchants")

    shipping_zone = models.ManyToManyField(ship.ShippingZone, related_name="merchants")

    status = models.CharField(max_length=5, choices=MERCHANT_ACCOUNT_STATUS)

    def is_active(self):
        return self.status == ACTIVE


class MerchantProfile(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    company_name = models.CharField(max_length=30)
    company_desc = models.CharField(max_length=200)
    company_web_link = models.URLField(verbose_name="company website")
    company_image = models.ImageField(verbose_name="company image")
    company_email = models.EmailField()
    street_address_1 = models.CharField(max_length=256, blank=True)
    street_address_2 = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    city_area = models.CharField(max_length=128, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = CountryField()
    country_area = models.CharField(max_length=128, blank=True)
    #phone = PossiblePhoneNumberField(blank=True, default='')

    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE, to_field="uuid", null=True, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "Merchant Profiles"
        verbose_name = "Merchant Profile"
