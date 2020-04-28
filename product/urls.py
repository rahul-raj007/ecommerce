from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    
    path("product/", views.productView, name="productview"),
    path("product/<slug:slug>/", views.productDetailsview, name="details")
]
