from django.shortcuts import redirect
from django.db import models
from product.models import Product
from django.db.models import Count
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    def searchcart(self, sessionid):
        return self.get(id=sessionid)

    def cartcreated(self, request):
        sessionid = request.session.get("sessionid", None)
        if sessionid is not None:
            try:
                cart = self.searchcart(sessionid)
            except ObjectDoesNotExist:
                print("the cart has been deleted")
                print(
                    "creating new cart with the updating session id and associating user")
                cart = self.creatcart(user=request.user)
                request.session["sessionid"] = cart.id
            else:
                if request.user.is_authenticated:
                    user_cart = self.filter(
                        user=request.user, active_cart=True)
                    user_active_cart = user_cart.last()
                    user_cart_exists = user_cart.exists()

                    if cart.id != user_active_cart.id and user_cart_exists:
                        products = cart.product.all()
                        user_active_cart.product.add(
                            *products)
                        cart.delete()
                        cart = user_active_cart
                        request.session["sessionid"] = user_active_cart.id
                    else:
                        if cart.user != request.user:
                            cart.save()

            request.session["totalNumberOfProduct"] = cart.product.count()
        else:
            cart = self.creatcart(user=None)
            request.session["sessionid"] = cart.id

        return cart

    def creatcart(self,  user=None,):
        cartuser = None
        if user is not None:
            cartuser = user
        return self.create(user=cartuser)

    def updatecart(self, request, additem=None, removeitem=None):
        cart = self.cartcreated(request)
        if additem is not None:
            try:
                prod = Product.objects.get(slug=additem)
                cart.product.add(prod)
                request.session["totalNumberOfProduct"] += 1
            except ObjectDoesNotExist:
                print("product doesnot exists")
            else:
                added = True
                return redirect("product:details", slug=additem), added
        if removeitem is not None:

            try:
                prod = Product.objects.get(slug=removeitem)
                cart.product.remove(prod)
                request.session["totalNumberOfProduct"] -= 1

            except ObjectDoesNotExist:
                print("product doesnot exists")
            else:
                added = False
                return redirect("product:details", slug=removeitem), added


class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(
        max_digits=7, decimal_places=2, default=100)
    updated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)
    subtotals = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, default=5)
    active_cart = models.BooleanField(default=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    def deactivate_active_cart(self):
        self.active_cart = False
        self.save()
