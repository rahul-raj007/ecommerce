# from django.db.models.signals import m2m_changed


def m2m_product_changed_signals(sender, instance, action, *args, **kwargs):
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        product = instance.product.all()
        total = 0
        for obj in product:
            total += obj.price
        instance.subtotals=total
        instance.total=total+12
        instance.save()
        


