# from orders.models import OrderForRegisterUser, OrderForAnonymusUser
import stripe
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

stripe.api_key = 'sk_test_YFHkpuonyl6Fbooq7eqAeHVW00FwZsUrgu'
# Create your models here.

# def get_user():
#     return get_user_model().objects.(username="deleted")


class BillingProfileforRegisterUser(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.SET_DEFAULT, default='deleted')
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Biiling Profile For Register User"


class BillingProfileForAnonymous(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    customer_id = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Billing Profile For Anonymous User"


class CardManager(models.Manager):
    def create_new_card(self, Billing_obj, stripe_respose):
        if str(stripe_respose.object) == "card":
            new_card = self.model(
                stripe_id=stripe_respose.id,
                country_id=stripe_respose.country,
                brand=stripe_respose.brand,
                card_type=stripe_respose.funding,
                exp_month=stripe_respose.exp_month,
                exp_year=stripe_respose.exp_year,
                cadr_last4_digit=stripe_respose.last4,
                cust_id=Billing_obj
            )
            new_card.save()
            return new_card


class UserCard(models.Model):
    stripe_id = models.CharField(max_length=100)
    country_id = models.CharField(max_length=2)
    brand = models.CharField(max_length=10)
    card_type = models.CharField(max_length=20)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    cadr_last4_digit = models.IntegerField()

    objects = CardManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.cust_id.email+self.stripe_id


class UserCardForAnonymusUser(UserCard):
    cust_id = models.ForeignKey(
        BillingProfileForAnonymous,
        on_delete=models.CASCADE
    )


class UserCardForRegisterUser(UserCard):
    cust_id = models.ForeignKey(
        BillingProfileforRegisterUser,
        on_delete=models.CASCADE
    )


class chargeManagerForRegisterUser(models.Manager):
    def create_charge(self, billing_profile_email, order_obj):
        customer = BillingProfileforRegisterUser.objects.get(
            email=billing_profile_email)
        card = UserCardForRegisterUser.objects.filter(
            cust_id__email=billing_profile_email).first().stripe_id

        charge_response = stripe.Charge.create(
            amount=int(order_obj.total*100),
            currency="inr",
            customer=customer.customer_id,
            source=card,
            description="My First Test Charge (created for API docs)",
        )
        new_charge_obj = self.model(
            billing_profile=customer,
            stripe_id=charge_response.id,
            paid=charge_response.paid,
            refunded=charge_response.amount_refunded,
            outcome=charge_response.outcome,
            outcome_type=charge_response.outcome["type"],
            seller_message=charge_response.outcome["seller_message"],
            risk_level=charge_response.outcome["risk_level"]
        )
        new_charge_obj.save()
        return new_charge_obj


class chargeManagerForAnonymousUser(models.Manager):
    def create_charge(self, billing_profile_email, order_obj):
        customer = BillingProfileForAnonymous.objects.get(
            email=billing_profile_email)
        card = UserCardForAnonymusUser.objects.filter(
            cust_id__email=billing_profile_email).first().stripe_id

        charge_response = stripe.Charge.create(
            amount=int(order_obj.total*100),
            currency="inr",
            customer=customer.customer_id,
            source=card,
            description="My First Test Charge (created for API docs)",
        )
        new_charge_obj = self.model(
            billing_profile=customer,
            stripe_id=charge_response.id,
            paid=charge_response.paid,
            refunded=charge_response.amount_refunded,
            outcome=charge_response.outcome,
            outcome_type=charge_response.outcome["type"],
            seller_message=charge_response.outcome["seller_message"],
            risk_level=charge_response.outcome["risk_level"]
        )
        new_charge_obj.save()
        return new_charge_obj


class ChargeForRegisterUser(models.Model):
    billing_profile = models.ForeignKey(
        BillingProfileforRegisterUser, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=120, null=True, blank=True)
    seller_message = models.CharField(max_length=120, null=True, blank=True)
    risk_level = models.CharField(max_length=120, null=True, blank=True)

    objects = chargeManagerForRegisterUser()


class ChargeForAnonymousUser(models.Model):
    billing_profile = models.ForeignKey(
        BillingProfileForAnonymous, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    outcome = models.TextField(null=True, blank=True)
    outcome_type = models.CharField(max_length=120, null=True, blank=True)
    seller_message = models.CharField(max_length=120, null=True, blank=True)
    risk_level = models.CharField(max_length=120, null=True, blank=True)

    objects = chargeManagerForAnonymousUser()
