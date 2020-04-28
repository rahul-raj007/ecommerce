from django.apps import AppConfig
from django.db.models.signals import pre_save


class OrdersConfig(AppConfig):
    name = 'orders'

    def ready(self):
        registeruser = self.get_model("OrderForRegisterUser")
        anonymususer = self.get_model("OrderForAnonymusUser")
        from .signals import pre_save_order_id, pre_save_ordertotal
        pre_save.connect(receiver=pre_save_order_id, sender=registeruser)
        pre_save.connect(receiver=pre_save_ordertotal, sender=registeruser)
        pre_save.connect(receiver=pre_save_order_id, sender=anonymususer)
        pre_save.connect(receiver=pre_save_ordertotal, sender=anonymususer)
