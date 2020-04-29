from django.shortcuts import render
from .forms import ContactMessageForm
# from contact_us.models import ContactMessage


def contact_message_creations(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactMessageForm()
    context = {"form": form}

    return render(request, "contact_us/contact_us.html", context)

