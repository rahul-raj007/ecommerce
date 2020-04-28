from django import forms
from .models import User, UserProfile
from django.contrib.auth.forms import ReadOnlyPasswordHashField
import string
from datetime import date
from bootstrap_datepicker_plus import DatePickerInput

from django.conf import settings


class UserCreationFormInAdmin(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput, max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="confirm password"
    )

    class Meta:
        model = User
        fields = ("email", "password", "password2", "active", "admin", "staff")

    def clean(self):
        cleaned_data = super(UserCreationFormInAdmin, self).clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("password don't match")

    def save(self, commit=True):
        user = super(UserCreationFormInAdmin, self).save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class UserEditChangeFormInAdmin(forms.ModelForm):
    # password1=forms.CharField(label="password",widget=forms.PasswordInput)
    # password2=forms.CharField(label="confirm password",widget=forms.PasswordInput)
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "active", "admin", "staff")


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "email",
            "class": "form-control",
            "aria-describedby": "emailHelp"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "passwords",
            "class": "form-control"
        }
    ))


class UserRegisterForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "First Name",
            "class": "form-control",
            "required": ""
        }
    ))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "placeholder": "Last Name",
            "class": "form-control",
            "required": ""
        }
    ))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={
            "placeholder": "Email",
            "class": "form-control",
            "required": ""
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "password",
            "class": "form-control",
            "required": ""
        }
    ))
    confirm_Password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "confirm password",
            "class": "form-control",
            "required": ""

        }
    ))

    # def clean(self):
    #     cleaned_data = super(UserRegisterForm, self).clean()
    #     password = cleaned_data.get("password")
    #     password2 = cleaned_data.get("confirm_Password")
    #     if password != password2:
    #         raise forms.ValidationError(
    #             "Password and Confirm Password Must be Same")

    #     return cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError(
                "Password length must be of 8 or More Character long")
        else:
            splited_password = [i for i in password]
            letters = [i.isupper() for i in splited_password]
            if not any(letters):
                raise forms.ValidationError(
                    "Must have a char in [A-z,a-z,0-9,special char]")
        return password

    def clean_confirm_Password(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("confirm_Password")
        
        if password != password2:
            raise forms.ValidationError(
                "Password and Confirm Password Must be Same")

    class Meta:
        model = User
        fields = "__all__"


class DateInput(forms.DateInput):
    input_type = "date"


class UserProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    country = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control"
    }))
    DOB = forms.DateField(widget=DatePickerInput(format='%d-%m-%Y'))
    profile_pic = forms.ImageField(widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'DOB',
                  'state', 'country', 'profile_pic')

    # def save(self, commit=True):
    #     cleaned_data = super().save(commit=False)
    #     cleaned_data.user = self.request.user
    #     if commit:
    #         cleaned_data.save()
    #     return cleaned_data
