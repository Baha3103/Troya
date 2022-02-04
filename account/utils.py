from django.core.mail import send_mail


def send_welcome_email(email):
    message = f'Dear {email}, thank you for registration on our site Furniture Shop!'
    send_mail(
        'Welcome to Furniture Shop!',
        message,
        'furniture@gmail.com',
        [email],
        fail_silently=False
    )
