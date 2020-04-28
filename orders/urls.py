from django.urls import path

from . import views

app_name = "orders"
urlpatterns = [
    path("checkout/orderdetails/", views.orderdetails, name="ordersdetails"),
    path("final/checkout",views.final_checkout,name="finalcheckout")
]
