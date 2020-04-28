from django.urls import path
from . import views


app_name = "address"

urlpatterns = [
    path("", views.address_creations, name="authenticated_address"),
    path("anonymus/", views.address_creations_for_anonymus,
         name="anonymus_address_creation"),
    path("addresses-shipping/", views.dispaly_shipping_available_addres,
         name="shipping_address"),
    path("addresses-billing/", views.dispaly_billing_available_addres,
         name="billing_address"),

]
