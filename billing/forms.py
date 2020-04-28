from django import forms
from .models import BillingProfileForAnonymous


class Billing_FormForAnonymusUser(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "First Name"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Last Name"
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "example@gmail.com"
    }))

    class Meta:
        model = BillingProfileForAnonymous
        fields = ("first_name", "last_name", "email")
