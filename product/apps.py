from django.apps import AppConfig
# from .signals import slugifyFields
''' never import anything from anyapp but django'''
from django.db.models.signals import pre_save


class ProductConfig(AppConfig):
    name = 'product'
    lable = "product"

    def ready(self):
        from .signals import slugifyFields
        from .models import Product
        mymodel = self.get_model("Product")
        pre_save.connect(slugifyFields, Product)
        # pre_save.connect(slugifyFields, mymodel) other valid way to connect signals
