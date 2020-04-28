from django.shortcuts import render, redirect
from .models import Product
from cart.models import Cart
from django.utils.http import is_safe_url
# Create your views here.


def productView(request):
    products = Product.objects.all()
    return render(request, "product/product.html", {"product": products})


def productDetailsview(request, slug):
    # print(request.META['HTTP_REFERER']) will get the previous url from where we have forwarded to this page
    print(request.GET.get('next'))
    print(request.get_host())
    product = Product.objects.get(slug=slug)
    cart = Cart.objects.cartcreated(request)
    cartitem = cart.product.all()
    context = {"cartitem": cartitem, "product": product}
    return render(request, "product/product_details.html", context)
