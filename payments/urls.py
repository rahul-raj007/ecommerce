from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("", views.payment_page, name="payment_page"),
    path("payment/card-created/done/", views.create_payment_card, name="successfull"),
    path("payment/successfull/",views.charging_customer,name="done_payment"),
]
