from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

def create_activation_link(user):
    """Creates an activation link for the confirmation email"""

    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f'localhost:8000/api/auth/activate/{uidb64}/{token}/'

    return activation_link

def send_activation_email(email, first_name, activation_link):
    """Creates an email and sends it to the registered user"""
    subject = 'Activate your account'
    from_email = 'no-replay@dabubble.de'
    to = [email]
    context = {
        'first_name': first_name,
        'activation_link': activation_link
    }

    body = render_to_string('auth_api/emails/confirm_email.html', context)


    msg = EmailMessage(subject, body, from_email, to)
    msg.send()