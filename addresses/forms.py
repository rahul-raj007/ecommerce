from django import forms
from .models import Addresses, AddressForAnonymusUser


class AddressForms(forms.ModelForm):
    address_line_1 = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "House No./Flat NO."
        }
    ))
    address_line_2 = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Area/Locality."
        }
    ))
    city = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "City e.g-Bengaluru,Delhi"
        }
    ))
    country = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "e.g- India,America"
        }
    ))
    state = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "e.g-Karnataka,Andhra Pradesh"
        }
    ))
    postal = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "PIN,e.g-548916"
        }
    ))

    class Meta:
        model = Addresses
        fields = ("address_line_1", "address_line_2",
                  "city", "country", "state", "postal")


class AddressFormForAnonymus(AddressForms):

    class Meta:
        model = AddressForAnonymusUser
        fields = ("address_line_1", "address_line_2",
                  "city", "country", "state", "postal")
