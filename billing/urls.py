from django.urls import path
from . import views

app_name = "billing"

urlpatterns = [
    path("login", views.billinglogin, name="login") ,
    path('login/anonymous', views.billingloginforanonymoususer, name="anonymous")
]
