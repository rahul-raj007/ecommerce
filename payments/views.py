import stripe
from django.shortcuts import render, redirect
from orders.models import OrderForRegisterUser, OrderForAnonymusUser
from django.http import HttpResponse
from billing.models import (BillingProfileforRegisterUser,
                            BillingProfileForAnonymous,
                            UserCardForRegisterUser,
                            UserCardForAnonymusUser,
                            ChargeForRegisterUser,
                            ChargeForAnonymousUser
                            )
from django.http import HttpResponse, JsonResponse

STRIPE_SK_KEY = 'sk_test_YFHkpuonyl6Fbooq7eqAeHVW00FwZsUrgu'
STRIPE_PK_KEY = "pk_test_CuZzPUIBg30kiXWesiltt2ms00R6HGBNRn"


# Create your views here.

def payment_page(request):
    return render(request, 'stripe/stripe.html', {'pub_key': STRIPE_PK_KEY})


def create_payment_card(request):
    if request.method == "POST" and request.is_ajax():
        if request.user.is_authenticated:
            billing_obj = BillingProfileforRegisterUser.objects.get(
                user=request.user)
            token = request.POST.get("token")
            card = UserCardForRegisterUser.objects.filter(
                cust_id__email=request.user.email)
            print(card)
            if card.count() == 0:
                if token is not None:
                    customer = stripe.Customer.retrieve(
                        billing_obj.customer_id)
                    stripe_response = customer.sources.create(source=token)
                    UserCardForRegisterUser.objects.create_new_card(
                        billing_obj,
                        stripe_response
                    )
            return redirect("payment:done_payment")
        if request.user.is_anonymous:
            anonymus_email = request.session.get("anonymoususer")
            billing_obj = BillingProfileForAnonymous.objects.get(
                email=anonymus_email)
            token = request.POST.get("token")
            if token is not None:
                customer = stripe.Customer.retrieve(billing_obj.customer_id)
                stripe_response = customer.sources.create(source=token)
                UserCardForAnonymusUser.objects.create_new_card(
                    billing_obj,
                    stripe_response
                )

            return redirect("payment:done_payment")
            print("hello bhai")
    return render(request, 'stripe/stripe.html', {'pub_key': STRIPE_PK_KEY})


def deactivate_and_delete_session_keys(order_obj, request):
    order_obj.cart.deactivate_active_cart()
    request.session.__delitem__("sessionid")
    request.session.__delitem__("totalNumberOfProduct")
    request.session.__delitem__("order_id")
    request.session.__delitem__("shipping_id")
    if request.session.get('anonymoususer') is not None:
        request.session.__delitem__("anonymoususer")


def charging_customer(request):
    message = "Thank you,Your Order has been placed successfully"
    context = {"message": message}

    if request.user.is_authenticated:
        order_id = request.session.get("order_id")
        order_obj = OrderForRegisterUser.objects.get(order_id=order_id)
        ChargeForRegisterUser.objects.create_charge(
            request.user.email, order_obj)
        deactivate_and_delete_session_keys(order_obj, request)
        print("working")
        return JsonResponse(context)
        # return render(request, 'stripe/successfull.html', context)

    if request.user.is_anonymous:
        order_id = request.session.get("order_id")
        anonymus_email = request.session.__getitem__("anonymoususer")

        order_obj = OrderForAnonymusUser.objects.get(order_id=order_id)
        ChargeForAnonymousUser.objects.create_charge(
            anonymus_email, order_obj)
        deactivate_and_delete_session_keys(order_obj, request)
        print("working")
        return JsonResponse(context)

        # return render(request, 'stripe/successfull.html', context)
