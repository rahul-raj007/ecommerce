from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserEditChangeFormInAdmin, UserCreationFormInAdmin
from .models import UserProfile
User = get_user_model()


# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserEditChangeFormInAdmin  # this is edit from in admin panel
    add_form = UserCreationFormInAdmin  # this is user creations forms in admin
    list_display = ("email", "first_name", "last_name", 'admin')
    list_filter = ('admin', "active", "staff")
    ordering = ('email',)
    filter_horizontal = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal information', {'fields': ('first_name', 'last_name')}),
        # ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('admin',)}),
        ('Important Date', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2',)}
         ),
        ('Personal information', {'fields': ('first_name', 'last_name')}),
        ('Permission', {'fields': ("active", "admin", "staff")})
    )


class UserprofileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'DOB']
    ordering = ('first_name',)
    list_filter = ()
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserprofileAdmin)
admin.site.site_header = "Ecommerce Project"
admin.site.site_title = "Ecommerce|Admin"
admin.site.index_title = "Welcome to project"
