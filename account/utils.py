from django.core.mail import send_mail


def send_welcome_email(email):
    message = f'{email}, thank you for registration!'
    send_mail(
        'Welcome!',
        message,
        '',
        [email],
        fail_silently=False
    )
