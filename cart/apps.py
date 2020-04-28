from django.apps import AppConfig
from django.db.models.signals import m2m_changed


class CartConfig(AppConfig):
    name = 'cart'

    def ready(self):
        from.signals import m2m_product_changed_signals
        from .models import Cart
        mymodel = self.get_model("cart")


        m2m_changed.connect(receiver=m2m_product_changed_signals,
                            sender=Cart.product.through)
