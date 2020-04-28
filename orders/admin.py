from django.contrib import admin
from .models import OrderForAnonymusUser, OrderForRegisterUser
# Register your models here.

admin.site.register(OrderForRegisterUser)
admin.site.register(OrderForAnonymusUser)
