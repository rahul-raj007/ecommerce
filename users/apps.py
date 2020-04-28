from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        mymodel = self.get_model("User")
        from .signals import login_signals_to_clear_current_session_key, post_save_Profile_creation
        user_logged_in.connect(login_signals_to_clear_current_session_key)
        post_save.connect(receiver=post_save_Profile_creation,sender=mymodel)
