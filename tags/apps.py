from django.apps import AppConfig
from django.db.models.signals import pre_save


class TagsConfig(AppConfig):
    name = 'tags'

    def ready(self):
        # from product.signals import slugifyFields
        # from ecommerce  import .product.signals
        from product.signals import slugifyFields
        mymodel = self.get_model("tags")

        print(mymodel)

        pre_save.connect(slugifyFields, mymodel)
