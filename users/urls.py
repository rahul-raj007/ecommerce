from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("login/", views.user_login, name="login_url"),
    path("register", views.user_register, name="user_register"),
    path("logout/", views.logoutfunction, name="logout"),
    path("profile/", views.display_profile, name="display_profile"),
    path("update/profile/<str:unique_id>",
         views.update_user_profile, name="update_profile")
]
