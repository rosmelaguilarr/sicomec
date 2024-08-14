from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .utils import check_expirations

@receiver(user_logged_in)
def on_user_login(sender, request, user, **kwargs):
    check_expirations()
