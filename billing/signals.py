from .models import BillingProfileforRegisterUser
import stripe
stripe.api_key = 'sk_test_YFHkpuonyl6Fbooq7eqAeHVW00FwZsUrgu'


def post_save_billing_profile_for_user(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfileforRegisterUser.objects.create(
            user=instance, email=instance.email)


def pre_save_stripe_customer_id_creation(sender, instance, *agrs, **kwargs):
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(
            email=instance.email
        )
        instance.customer_id = customer.id
