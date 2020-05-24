from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template import loader

from .models import User, UserPreferences
from .utils import send_welcome_email


@receiver(post_save, sender=User)
def setup_user_account(sender, instance, created, **kwargs):
    """
    Send a new User a welcome email as well as creating a Profile model.
    """
    if created:
        UserPreferences.objects.create(user=instance)
        # send_welcome_email(instance)