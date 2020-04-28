from django.shortcuts import render, reverse
from django.http import HttpResponse
from .models import OrderForRegisterUser, OrderForAnonymusUser
from django.urls import get_resolver
from django.utils.http import is_safe_url
from cart.models import Cart
from django.core.exceptions import ObjectDoesNotExist
from billing.models import BillingProfileforRegisterUser, BillingProfileForAnonymous
from django.shortcuts import redirect
from django.conf import settings
from addresses.models import Addresses, AddressForAnonymusUser
from addresses.views import dispaly_billing_available_addres

User = settings.AUTH_USER_MODEL

# Create your views here.


def orderdetails(request):
    previous_route = request.META.get("HTTP_REFERER", None)
    matcing_url = request.get_full_path
    cart_id = request.session.get("sessionid", None)
    anonymous_email = request.session.get("anonymoususer", None)
    user = request.user
    if previous_route:
        if request.user.is_authenticated and cart_id is not None:
            try:
                cart_obj_for_register_user = Cart.objects.get(id=cart_id)
                cart_obj_for_register_user.user = request.user
                cart_obj_for_register_user.save()
                try:
                    billing_obj = BillingProfileforRegisterUser.objects.get(
                        user__id=request.user.id)

                    orders_obj, created = OrderForRegisterUser.objects.update_or_create(
                        cart=Cart(id=cart_id),
                        defaults={
                            "billing_profile_register_user": billing_obj
                        }

                    )
                    cart = Cart.objects.get(id=cart_id)
                    subtotal = cart.subtotals
                    total = cart.total
                    product = cart.product.all()
                except ObjectDoesNotExist:
                    print(
                        "billing object has not been created yet for authenticated users")
            except ObjectDoesNotExist:
                print(" Cart doesn't exists ")
        else:
            try:
                cart_obj_for_anonymus_user = Cart.objects.get(id=cart_id)
                try:
                    billing_obj = BillingProfileForAnonymous.objects.get(
                        email=anonymous_email)

                    orders_obj, created = OrderForAnonymusUser.objects.update_or_create(
                        cart=Cart(id=cart_id),
                        defaults={
                            "billing_profile_anynous_user": billing_obj
                        }
                    )
                    cart = Cart.objects.get(id=cart_id)
                    subtotal = cart.subtotals
                    total = cart.total
                    product = cart.product.all()
                except ObjectDoesNotExist:
                    print("billing object for anonymus user doesn't exists")
            except ObjectDoesNotExist:
                print("cart doesn't exist for anonymus user")
        a = orders_obj
        request.session["order_id"] = orders_obj.order_id
        context = {"order_info": orders_obj, "product": product,
                   "total": total, "subtotal": subtotal}
        return render(request, "order/orderdetails.html", context)
    return redirect("cart:cartitem")


def final_checkout(request):
    # prev = request.META.get("HTTP_REFERER", None)
    if request.method == "POST":
        billing_address_id = request.POST.get("billing_address")
        shipping_address_id = request.session.get('shipping_id')

        if request.user.is_authenticated:
            try:
                shipping_address = Addresses.objects.get(
                    # id=shipping_address_id,
                    id=shipping_address_id,
                    billing_address__user=request.user,
                    address_type="shipping"
                )
                try:
                    billing_address = Addresses.objects.get(
                        id=billing_address_id,
                        billing_address__user=request.user,
                        address_type="billing"
                    )
                except ObjectDoesNotExist:
                    print("billing address for the given user doesn't exists")
            except ObjectDoesNotExist:
                print("Shipping Address for the given user doesn't exists")
            else:
                order_id = request.session.get("order_id")
                order_obj = OrderForRegisterUser.objects.get(order_id=order_id)
                order_obj.billing_address = billing_address
                order_obj.shipping_address = shipping_address
                order_obj.save()
        else:
            try:
                anonymus_email = request.session.get("anonymoususer", None)
                shipping_address = AddressForAnonymusUser.objects.get(
                    id=shipping_address_id,
                    billing_address__email=anonymus_email,
                    address_type="shipping"
                )
                try:
                    billing_address = AddressForAnonymusUser.objects.get(
                        id=billing_address_id,
                        billing_address__email=anonymus_email,
                        address_type="billing"
                    )
                except ObjectDoesNotExist:
                    print("billing address for the given user doesn't exists")
            except ObjectDoesNotExist:
                print("Shipping Address for the given user doesn't exists")
            else:
                order_id = request.session.get("order_id")
                order_obj = OrderForAnonymusUser.objects.get(order_id=order_id)
                order_obj.billing_address = billing_address
                order_obj.shipping_address = shipping_address
                order_obj.save()
        product = order_obj.cart.product.all()
        session_keys = request.session.keys()
        print(session_keys)

        context = {"order_obj": order_obj, "product": product}
        return render(request, "order/finalcheckoutorder.html", context)
    else:
        return redirect("address:billing_address")
