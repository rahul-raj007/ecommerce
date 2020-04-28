from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import settings
from django.utils.http import is_safe_url
from .forms import Billing_FormForAnonymusUser
from .models import BillingProfileForAnonymous, BillingProfileforRegisterUser
# from django.core.exceptions import ValidationError
# from django.conf import settings
# from .urls import urlpatterns


# Create your views here.
# print(urlpatterns)


def billinglogin(request):
    previous_reference = request.META.get('HTTP_REFERER', None)
    request.session['next'] = request.build_absolute_uri()
    form = Billing_FormForAnonymusUser()
    if previous_reference:
        if request.user.is_authenticated:
            del request.session["next"]
            return redirect("orders:ordersdetails")
        elif request.user.is_anonymous:
            form = Billing_FormForAnonymusUser()
            context = {"form": form}
            return render(request, "billing/billinglogin.html", context)
    elif previous_reference is None:
        return redirect("cart:cartitem")


def billingloginforanonymoususer(request):
    print(request.method)
    if request.method == "POST":
        form = Billing_FormForAnonymusUser(request.POST)
        name = request.POST.get("email")
       
        if form.is_valid():
            request.session["anonymoususer"] = form.cleaned_data.get(
                "email")
            billing_obj, created = BillingProfileForAnonymous.objects.get_or_create(
                **form.cleaned_data)
            request.session["anonymoususer"] = form.cleaned_data.get(
                "email")
            return redirect("orders:ordersdetails")

        billing_obj = BillingProfileForAnonymous.objects.get(email=name)
        if billing_obj:
            request.session["anonymoususer"] = name
            return redirect("orders:ordersdetails")
        if form.errors:
            print(form.errors.as_data())
    else:
        form = Billing_FormForAnonymusUser()
    context = {"form": form}
    return render(request, "billing/billinglogin.html")
