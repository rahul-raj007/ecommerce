from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm, UserProfileUpdateForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import is_safe_url
from django.contrib import messages
from .models import UserProfile
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def user_login(request):
    previous_reference = request.META.get('HTTP_REFERER', None)
    deta = request.session.get('next')
    print("working")
    if deta is not None and is_safe_url(deta, request.get_host()):
        print(" not working")
        if request.method == "POST":
            forms = UserLoginForm(request.POST)
            if forms.is_valid():
                user = authenticate(email=forms.cleaned_data.get(
                    "email"), password=forms.cleaned_data.get("password"))
                if user is not None:
                    login(request, user)
                    return redirect(deta)

    elif request.method == "POST":
        forms = UserLoginForm(request.POST)
        if forms.is_valid():
            user = authenticate(email=forms.cleaned_data.get(
                "email"), password=forms.cleaned_data.get("password"))
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                messages.error(
                    request, "Email or Password May Not Be Correct.")

    forms = UserLoginForm()
    return render(request, "Users/login.html", {"form": forms})


def user_register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            get_user_model().objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

        if form.errors:
            print(form.errors.as_data())
    else:
        form = UserRegisterForm()
    return render(request, "Users/register.html", {"form": form})


def logoutfunction(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def display_profile(request):
    try:
        user = UserProfile.objects.get(user=request.user)
        print(user.DOB)
    except ObjectDoesNotExist:
        print("User Profile doesn't exists")
    return render(request, "Users/view_profile.html", {"user": user})


def update_user_profile(request, unique_id):
    print(dir(request))
    if request.method == "POST":
        user = UserProfile.objects.get(unique_id=unique_id)
        form = UserProfileUpdateForm(
            request.POST, request.FILES, instance=user,)
        if form.is_valid():
            form.save()
            return redirect("user:update_profile", unique_id=unique_id)
        if form.errors:
            print(form.errors.as_data())
    else:
        user = UserProfile.objects.get(unique_id=unique_id)
        form = UserProfileUpdateForm(instance=user)
    return render(request, 'Users/profile_update.html', {"form": form})


