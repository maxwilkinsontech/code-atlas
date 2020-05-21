from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.dispatch import receiver
from django.template import loader

from .models import User, Profile


@receiver(post_save, sender=User)
def setup_user_account(sender, instance, created, **kwargs):
    """
    Send a new User a welcome email as well as creating a Profile model.
    """
    if created:
        Profile.objects.create(user=instance)
        # subject = 'Welcome to Code Atlas'
        # body = 'Welcome to Code Atlas'

        # email_message = EmailMultiAlternatives(
        #     subject, 
        #     body, 
        #     'noreply@code-atlas.me', 
        #     [instance.email]
        # )
        # html_email = loader.render_to_string('email/welcome.html')
        # email_message.attach_alternative(html_email, 'text/html')
        # email_message.send()