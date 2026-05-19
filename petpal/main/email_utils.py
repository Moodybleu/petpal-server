import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from django.conf import settings
from django.core.mail import send_mail


class EmailNotConfiguredError(Exception):
    """Raised when production has no real email provider configured."""


class EmailDeliveryError(Exception):
    """Raised when an email provider rejects or fails the send."""


def is_email_configured() -> bool:
    if getattr(settings, 'RESEND_API_KEY', ''):
        return True
    if getattr(settings, 'EMAIL_HOST', ''):
        return True
    if settings.DEBUG:
        return True
    return False


def _send_via_resend(to_email: str, subject: str, message: str) -> None:
    api_key = settings.RESEND_API_KEY
    from_email = settings.DEFAULT_FROM_EMAIL
    payload = json.dumps({
        'from': from_email,
        'to': [to_email],
        'subject': subject,
        'text': message,
    }).encode()
    request = Request(
        'https://api.resend.com/emails',
        data=payload,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    try:
        with urlopen(request, timeout=30) as response:
            if response.status >= 400:
                raise EmailDeliveryError(f'Resend returned status {response.status}')
    except HTTPError as err:
        body = err.read().decode()
        raise EmailDeliveryError(f'Resend error {err.code}: {body}') from err
    except URLError as err:
        raise EmailDeliveryError(str(err)) from err


def _deliver_email(to_email: str, subject: str, message: str) -> None:
    if not is_email_configured():
        raise EmailNotConfiguredError()

    if getattr(settings, 'RESEND_API_KEY', ''):
        _send_via_resend(to_email, subject, message)
        return

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )


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
    _deliver_email(user.email, subject, message)


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
    _deliver_email(user.email, subject, message)
