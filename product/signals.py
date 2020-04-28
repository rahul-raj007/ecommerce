import string
import random
# from django.db.models.signals import pre_save
# from .models import Product
from django.utils.text import slugify
# from django.dispatch import receiver


def random_string(size=10, char=string.ascii_lowercase+string.digits):
    created_string = ((random.choice(char)) for i in range(size))
    return "".join(created_string)


# @receiver(pre_save, sender=Product)
def slugifyFields(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    instanceClass = instance.__class__
    if not instanceClass.objects.filter(slug=slug).exists():
        instance.slug = slug
    else:
        instance.slug = slug + random_string()


# pre_save.connect(sender=Product)
