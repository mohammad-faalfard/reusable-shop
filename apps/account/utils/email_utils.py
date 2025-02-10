from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpRequest
from django.template.loader import render_to_string

from .static_utils import get_full_static_url


def send_forget_password_mail(request: HttpRequest, email: str, name: str, code: str) -> None:
    """
    Sends an email with a password reset code to the specified email address.

    Args:
        request (HttpRequest): The HTTP request object.
        email (str): Recipient's email address.
        name (str): Recipient's name.
        code (str): Password reset code to include in the email.

    Returns:
        None
    """
    template: str = "account/forget_password.template"
    subject: str = "Lost Your shop Password? No Worries!"
    context: dict = {
        "name": name,
        "code": code,
        "facebook_icon": get_full_static_url(request, "icons/facebook.png"),
        "instagram_icon": get_full_static_url(request, "icons/instagram.png"),
        "twitter_icon": get_full_static_url(request, "icons/twitter.png"),
        "shop_icon": get_full_static_url(request, "icons/shop.png"),
    }
    html_msg = render_to_string(template, context)

    send_mail(
        subject=subject,
        recipient_list=[email],
        html_message=html_msg,
        message=f"Your verification code is: {code}",
        from_email=settings.EMAIL_HOST_USER,
        fail_silently=True,
    )


def send_verify_email_mail(request: HttpRequest, email: str, name: str, code: str) -> None:
    """
    Sends a welcome email with a verification code to the specified email address.

    Args:
        request (HttpRequest): The HTTP request object.
        email (str): Recipient's email address.
        name (str): Recipient's name.
        code (str): Verification code to include in the email.

    Returns:
        None
    """
    template: str = "account/verify_email.template"
    subject: str = "Welcome to shop"
    context: dict = {
        "name": name,
        "code": code,
        "facebook_icon": get_full_static_url(request, "icons/facebook.png"),
        "instagram_icon": get_full_static_url(request, "icons/instagram.png"),
        "twitter_icon": get_full_static_url(request, "icons/twitter.png"),
        "shop_icon": get_full_static_url(request, "icons/shop.png"),
    }
    html_msg = render_to_string(template, context)

    send_mail(
        subject=subject,
        recipient_list=[email],
        html_message=html_msg,
        message=f"Your verification code is: {code}",
        from_email=settings.EMAIL_HOST_USER,
        fail_silently=True,
    )
