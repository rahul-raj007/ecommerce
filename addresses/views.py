from django.shortcuts import render, redirect, reverse
from .models import Addresses, AddressForAnonymusUser
from .forms import AddressForms, AddressFormForAnonymus
from orders.models import OrderForRegisterUser, OrderForAnonymusUser
from billing.models import BillingProfileforRegisterUser, BillingProfileForAnonymous
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def address_creations(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = AddressForms(request.POST)
            totaladdress = Addresses.objects.filter(
                billing_address__user=request.user)
            # if totaladdress.count() == 2:
            #     return redirect("orders:ordersdetails")
            if form.is_valid():
                address_type = request.POST.get("address_type", None)
                billing_obj = BillingProfileforRegisterUser.objects.get(
                    user=request.user)
                if address_type == "shipping":
                    instance = form.save(commit=False)
                    instance.billing_address = billing_obj
                    instance.address_type = "shipping"
                    instance.save()
                    return redirect("address:shipping_address")
                    form = AddressForms()
                    # next_address_type = "billing"
                    # context = {"form": form,
                    #            "next_address_type": next_address_type, }
                    # return render(request, "address/add_address.html", context)
                else:
                    if address_type == "billing":
                        instance = form.save(commit=False)
                        instance.billing_address = billing_obj
                        instance.address_type = "billing"
                        instance.save()
                        return redirect("address:billing_address")
    # else:
    #     if request.user.is_authenticated:
    #         shipping_addresses = Addresses.objects.filter(
    #             billing_address__user=request.user, address_type="shipping")
    #         forms = AddressForms()
    #         context = {"form": forms, "shipping": "shipping",
    #                    "shipping_addresses": shipping_addresses}
    return reverse("address:shipping_address")


def address_creations_for_anonymus(request):
    print(request.method)
    if request.method == "POST":
        form = AddressFormForAnonymus(request.POST)
        anonymus_email = request.session.get("anonymoususer", None)
        # anonymus_email = "rahulraj99ex@gmail.com"

        totaladdress = AddressForAnonymusUser.objects.filter(
            billing_address__email=anonymus_email)

        a = form.is_valid()
        print(a)
        if form.is_valid():
            address_type = request.POST.get("address_type", None)
            print(address_type)
            if anonymus_email:
                billing_obj = BillingProfileForAnonymous.objects.get(
                    email=anonymus_email)
                if address_type == "shipping":
                    instance = form.save(commit=False)
                    instance.billing_address = billing_obj
                    instance.address_type = "shipping"
                    instance.save()
                    # form = AddressFormForAnonymus()
                    # next_address_type = "billing"
                    # context = {"form": form,
                    #            "next_address_type": next_address_type}
                    return redirect("address:shipping_address")
                else:
                    if address_type == "billing":
                        instance = form.save(commit=False)
                        instance.billing_address = billing_obj
                        instance.address_type = "billing"
                        instance.save()
                        return redirect("address:billing_address")

            if form.errors:
                print(form.errors.as_data())
    return reverse("address:shipping_address")


def dispaly_shipping_available_addres(request):
    if request.user.is_authenticated:
        form = AddressForms()

        shipping_addresses = Addresses.objects.filter(
            billing_address__user=request.user, address_type="shipping")
    else:
        anonymus_email = request.session.get("anonymoususer", None)
        print(anonymus_email)
        form = AddressFormForAnonymus()

        # anonymus_email = "rahulraj99ex@gmail.com"
        if anonymus_email:
            shipping_addresses = AddressForAnonymusUser.objects.filter(
                billing_address__email=anonymus_email, address_type="shipping")
            print(shipping_addresses)
    address_type = "shipping"
    context = {"shipping_addresses": shipping_addresses,
               "form": form, "address_type": address_type}
    return render(request, 'address/shipping_address.html', context)


def dispaly_billing_available_addres(request):
    if request.method == "POST":
        request.session["shipping_id"] = request.POST.get("shipping_address")
    if request.user.is_authenticated:
        form = AddressForms()
        billing_addresses = Addresses.objects.filter(
            billing_address__user=request.user, address_type="billing")
    else:
        anonymus_email = request.session.get("anonymoususer", None)
        form = AddressFormForAnonymus()
        # anonymus_email = "rahulraj99ex@gmail.com"
        if anonymus_email:
            billing_addresses = AddressForAnonymusUser.objects.filter(
                billing_address__email=anonymus_email, address_type="billing")
            print(billing_addresses)
    address_type = "billing"
    context = {"billing_addresses": billing_addresses,
               "form": form, "address_type": address_type}
    return render(request, 'address/billing_address.html', context)
