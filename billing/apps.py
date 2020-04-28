from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save,pre_save


class BillingConfig(AppConfig):
    name = 'billing'

    def ready(self):
        from.signals import post_save_billing_profile_for_user, pre_save_stripe_customer_id_creation
        UserModel = get_user_model()
        registerusermodel = self.get_model("BillingProfileforRegisterUser")
        anonymususermodel = self.get_model("BillingProfileForAnonymous")
        post_save.connect(
            receiver=post_save_billing_profile_for_user, sender=UserModel)
        pre_save.connect(
            receiver=pre_save_stripe_customer_id_creation, sender=registerusermodel)
        pre_save.connect(
            receiver=pre_save_stripe_customer_id_creation, sender=anonymususermodel)
