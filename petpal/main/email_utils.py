from django.conf import settings
from django.core.mail import send_mail


def send_login_reminder_email(user, temporary_password: str) -> None:
    site_name = getattr(settings, 'PETPAL_SITE_NAME', 'Pet Pal')
    subject = f'{site_name} — your login information'
    message = (
        f'Hello,\n\n'
        f'You asked for help logging in to {site_name}. Here are your account details:\n\n'
        f'  Username: {user.name}\n'
        f'  Email: {user.email}\n'
        f'  Temporary password: {temporary_password}\n\n'
        f'Use your username or email with this temporary password to log in. '
        f'Consider choosing a new password you will remember after you sign in.\n\n'
        f'If you did not request this email, you can ignore it.\n'
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def send_password_reset_email(user) -> None:
    site_name = getattr(settings, 'PETPAL_SITE_NAME', 'Pet Pal')
    subject = f'{site_name} — your password was reset'
    message = (
        f'Hello,\n\n'
        f'Your {site_name} password was just changed using the reset form.\n\n'
        f'  Username: {user.name}\n'
        f'  Email: {user.email}\n\n'
        f'You can log in with your new password. If you did not do this, contact support.\n'
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
