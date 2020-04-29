from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Full Name"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Email"
    }))
    contact_message = forms.CharField(label="message",widget=forms.Textarea(attrs={
        "class": "form-control",
        "placeholder": "Your Message"
    }))

    class Meta:
        model = ContactMessage
        fields = ("full_name", "email", "contact_message")
