from .models import UserProfile
import string
import random


def login_signals_to_clear_current_session_key(sender, request, user, **kwargs):
    if request.method == "POST":
        try:
            keytodelte = request.session.__getitem__("next")
        except KeyError:
            print("key doesn't exist")
        else:
            request.session.__delitem__("next")

    print("keys cleared successfully ")


def unique_customer_id(id_length=10, char=string.digits+string.ascii_uppercase):
    unique_list = ((random.choice(char)) for i in range(id_length))
    unique_code = "".join(unique_list)
    return unique_code


def post_save_Profile_creation(sender, instance, created, *args, **kwargs):
    if created:
        profile = UserProfile.objects.create(
            user=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            unique_id=unique_customer_id()
        )
        profile.save()
