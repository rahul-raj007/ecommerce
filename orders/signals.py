from cart.models import Cart
import string
import random
from datetime import date


def unique_order_id(lengthofoutput=10, char=string.digits+string.ascii_uppercase):
    uniqueid = ((random.choice(char)) for _ in range(lengthofoutput))
    return "".join(uniqueid)


def pre_save_order_id(sender, instance, *args, **kwargs):
    if instance.order_id is None:
        date_today = date.today().strftime("%d%m%y")
        uniqueid = date_today+unique_order_id()
        instance.order_id = uniqueid


def pre_save_ordertotal(sender, instance, *args, **kwargs):
    cart_total = instance.cart.total
    instance.total = instance.delivery_cost+cart_total
