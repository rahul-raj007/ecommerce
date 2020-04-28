from django.db import models
from cart.models import Cart
from addresses.models import Addresses, AddressForAnonymusUser
from billing.models import BillingProfileforRegisterUser, BillingProfileForAnonymous
# from billing.models import
# from django.db.models.signals import p
# Create your models here.


ORDER_STATTUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)


class OrderForRegisterUser(models.Model):
    order_id = models.CharField(max_length=120, blank=True, null=True)
    billing_address = models.ForeignKey(
        Addresses,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,

        related_name="Billing_Address"
    )
    shipping_address = models.ForeignKey(
        Addresses,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        related_name="shipping_address"
    )

    billing_profile_register_user = models.ForeignKey(BillingProfileforRegisterUser,
                                                      on_delete=models.CASCADE,
                                                      verbose_name="For Registered User",
                                                      blank=True,
                                                      null=True,

                                                      )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=120,
        default='created',
        choices=ORDER_STATTUS_CHOICES
    )
    # shipping_total
    delivery_cost = models.DecimalField(
        default=25,
        max_digits=10,
        decimal_places=2
    )
    total = models.DecimalField(
        default=99,
        max_digits=10,
        decimal_places=2
    )
    active_order = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.cart.user}---{self.order_id}"


class OrderForAnonymusUser(models.Model):
    order_id = models.CharField(max_length=120, blank=True, null=True)
    billing_address = models.ForeignKey(
        AddressForAnonymusUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,

        related_name="Billing_Address"
    )
    shipping_address = models.ForeignKey(
        AddressForAnonymusUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        default=None,
        related_name="shipping_address"
    )

    billing_profile_anynous_user = models.ForeignKey(BillingProfileForAnonymous,
                                                     on_delete=models.CASCADE,
                                                     verbose_name="For Anynomus User",
                                                     blank=True,
                                                     null=True,

                                                     )
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=120,
        default='created',
        choices=ORDER_STATTUS_CHOICES
    )
    # shipping_total
    delivery_cost = models.DecimalField(
        default=25,
        max_digits=10,
        decimal_places=2
    )
    total = models.DecimalField(
        default=99,
        max_digits=10,
        decimal_places=2
    )
    active_order = models.BooleanField(default=True)

    def __str__(self):
        return self.billing_profile_anynous_user.first_name
