from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template import loader


def send_mail(subject, body, template, users):
    """
    Send an email to a list of Users.
    """
    subject = 'Welcome to Code Atlas'
    body = 'Welcome to Code Atlas'

    email_message = EmailMultiAlternatives(
        subject, 
        body, 
        'noreply@code-atlas.me', 
        users
    )
    html_email = loader.render_to_string(template)
    email_message.attach_alternative(html_email, 'text/html')
    email_message.send()