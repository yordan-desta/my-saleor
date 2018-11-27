import uuid as uuid
from django.db import models
from ..account import models as a_models
from ..shipping import models as ship

ACTIVE = 'A'
PENDING = 'P'
SUSPENDED = 'S'
CLOSED = 'C'
MERCHANT_ACCOUNT_STATUS = ((PENDING, "Pending"), (ACTIVE, "Active"), (SUSPENDED, "Suspended"), (CLOSED, "Closed"))


class AbstractModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key= True)
    created_on = models.DateTimeField(auto_now=True)
    modified_on = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-modified_on", ]
        abstract = True


class MerchantType(AbstractModel):
    vendor_type = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.vendor_type

    class Meta:
        verbose_name = "Vendor Type"
        verbose_name_plural = "Vendor Types"


class Merchant(AbstractModel):
    merchant_type = models.ForeignKey(MerchantType, on_delete=models.ProtectedError, to_field="uuid")

    shipping_method = models.ManyToManyField(ship.ShippingMethod, related_name="shipping_method",
                                             related_query_name="shipping_methods")

    shipping_zone = models.ManyToManyField(ship.ShippingZone, related_name="shipping_zone",
                                           related_query_name="shipping_zones")

    user = models.OneToOneField(a_models.User, on_delete=models.PROTECT, null=True)

    status = models.CharField(max_length=5, choices=MERCHANT_ACCOUNT_STATUS)

    def is_active(self):
        return self.status == ACTIVE


class MerchantProfile(AbstractModel):
    company_name = models.CharField(max_length=30)
    company_desc = models.CharField(max_length=200)
    company_web_link = models.URLField(verbose_name="company website")
    company_image = models.ImageField(verbose_name="company image")
    company_email = models.EmailField()
    company_phone = models.CharField(max_length=12)

    merchant = models.OneToOneField(Merchant, on_delete=models.CASCADE, to_field="uuid", null=True)

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name_plural = "Merchant Profiles"
        verbose_name = "Merchant Profile"
