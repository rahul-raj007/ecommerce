from django.shortcuts import render
from .models import Cart
from product.models import Product
from django.shortcuts import redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.http import JsonResponse
# Create your views here.


def cartItem(request):

    if request.method == "POST":
        itemToBeRemoved = request.POST.get("removeitem", None)
        Cart.objects.updatecart(
            request,
            removeitem=itemToBeRemoved
        )
    cart = Cart.objects.cartcreated(request)

    subtotal = cart.subtotals
    finaltotal = cart.total
    totalproduct = cart.product.all()
    context = {
        "product": totalproduct,
        "total": finaltotal,
        "subtotal": subtotal
    }

    return render(request, "cart/cart.html", context)


def updatecart(request):
    if request.method == "POST":
        itemToBeRemoved = request.POST.get("removeitem", None)
        itemToBeAdded = request.POST.get("additem", None)
        print("update_cart function run")
        print(f'removed items { itemToBeRemoved}')
        print(f'added items { itemToBeAdded}')
        path, added = Cart.objects.updatecart(
            request,
            additem=itemToBeAdded,
            removeitem=itemToBeRemoved
        )

    if request.is_ajax():
        
        jsondata = {
            "added": added,
            "totalitemincart": request.session.get("totalNumberOfProduct")
        }
        return JsonResponse(jsondata)
    else:
        if path:
            return path
    return redirect("cart:cartitem")

    """ if itemToBeRemoved:
            try:
                product = Product.objects.get(slug=itemToBeRemoved)
                cart.product.remove(product)
            except ObjectDoesNotExist:
                print("item doesnot exist")
            else:
                return redirect("product:details", slug=itemToBeRemoved)
        if itemToBeAdded:
            try:
                product = Product.objects.get(slug=itemToBeAdded)
                cart.product.add(product)
            except ObjectDoesNotExist:
                print("product doesnt exist")
            else:
                return redirect("product:details", slug=itemToBeAdded) """
    # return reverse("product:details", kwargs={"slug": itemToBeAdded})

    # return redirect("cart:cartitem")
    # cart, newcart = Cart.objects.new_or_create(request)


def cart_api(request):
    cart_obj = Cart.objects.cartcreated(request)
    products = cart_obj.product.all()
    product_array = []
    for x in products:
        product_array.append({
            "name": x.name,
            "price": x.price,
            "url": x.get_absolute_url(),
            "slug": x.slug
        })
    total_item_in_cart = len(product_array)
    total = cart_obj.total
    subtotal = cart_obj.subtotals
    json_data = {
        "products": product_array,
        "total": total,
        "subtotal": subtotal,
        "totalitem": total_item_in_cart
    }
    return JsonResponse(json_data)
