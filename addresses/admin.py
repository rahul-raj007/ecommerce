from django.contrib import admin
from .models import Addresses,AddressForAnonymusUser


# Register your models here.


admin.site.register(Addresses)
admin.site.register(AddressForAnonymusUser)
