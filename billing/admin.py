from django.contrib import admin
from.models import BillingProfileForAnonymous, BillingProfileforRegisterUser, UserCardForAnonymusUser, UserCardForRegisterUser,ChargeForAnonymousUser,ChargeForRegisterUser
# Register your models here.
admin.site.register(BillingProfileforRegisterUser)
admin.site.register(BillingProfileForAnonymous)
admin.site.register(UserCardForAnonymusUser)
admin.site.register(UserCardForRegisterUser)
admin.site.register(ChargeForRegisterUser)
admin.site.register(ChargeForAnonymousUser)
