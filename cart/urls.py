from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cartItem, name="cartitem"),
    path("update/", views.updatecart, name="updatecart"),
    path("cart-api/", views.cart_api, name="cart-api")
]
