from django.db import models
from billing.models import BillingProfileForAnonymous, BillingProfileforRegisterUser
# Create your models here.
ADDRESS_TYPE = (
    ('shipping', 'Shipping'),
    ('billing', 'Billing')
)


class Addresses(models.Model):
    billing_address = models.ForeignKey(
        BillingProfileforRegisterUser, on_delete=models.CASCADE, null=True, blank=True)
    address_type = models.CharField(
        max_length=225, choices=ADDRESS_TYPE, null=True, blank=True)
    address_line_1 = models.CharField(max_length=225, null=True, blank=True)
    address_line_2 = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    postal = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"{self.billing_address}  {self.address_type}"


class AddressForAnonymusUser(models.Model):
    billing_address = models.ForeignKey(
        BillingProfileForAnonymous, on_delete=models.CASCADE, null=True, blank=True)
    address_type = models.CharField(
        max_length=225, choices=ADDRESS_TYPE, null=True, blank=True)
    address_line_1 = models.CharField(max_length=225, null=True, blank=True)
    address_line_2 = models.CharField(max_length=225, null=True, blank=True)
    city = models.CharField(max_length=225, null=True, blank=True)
    country = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    postal = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return f"{self.billing_address}  {self.address_type}"
