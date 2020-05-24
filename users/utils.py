from core.utils import send_mail


def send_welcome_email(user):
    """
    Send a new User a welcome email.
    """
    subject = 'Welcome to Code Atlas'
    body = 'Welcome to Code Atlas'
    template = 'email/welcome.html'
    
    send_mail(subject, body, template, [user])