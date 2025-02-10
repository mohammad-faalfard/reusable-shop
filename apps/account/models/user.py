# apps/account/models/user.py

import string

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

from ..managers import UserManager
from .otp_mixin import OTPMixin


def generate_reset_password_token():
    """
    Generates a secure random string to be used as a password reset token.

    Returns:
        str: A random string of 50 characters containing letters.
    """
    return get_random_string(50, string.ascii_letters)


class User(OTPMixin, AbstractUser):
    """
    Custom User model extending Django's AbstractUser with additional fields and methods.

    Attributes:
        phone_number (str): User's phone number (optional, unique).
        is_verified_phone_number (bool): Flag indicating if the phone number is verified.
        email (str): User's email address (optional, unique).
        is_verified_email (bool): Flag indicating if the email address is verified.
        reset_password_token (str): Token for resetting the user's password.
        wallet (ForeignKey): Reference to the user's wallet.

    Methods:
        full_name: Returns the user's full name.
        is_completed_profile: Checks if the user's profile information is complete.
        set_reset_password_token: Generates a new reset password token.
        verify_email: Marks the user's email as verified.
        verify_phone_number: Marks the user's phone number as verified.
    """

    phone_number = models.CharField(
        _("Phone Number"),
        max_length=14,
        unique=True,
        null=True,
        blank=True,
    )
    is_verified_phone_number = models.BooleanField(
        _("Is Verified Phone Number"),
        default=False,
    )

    email = models.EmailField(
        _("Email"),
        max_length=254,
        blank=True,
        null=True,
    )
    is_verified_email = models.BooleanField(
        _("Is Verified Email"),
        default=False,
    )

    reset_password_token = models.CharField(
        _("Reset Password Token"),
        max_length=60,
        null=True,
        blank=True,
        default=None,
        unique=True,
        editable=False,
    )

    wallet = models.ForeignKey(
        "wallet.Wallet",
        verbose_name=_("Wallet"),
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return f"{self.username}"

    @property
    def full_name(self) -> str:
        """Concatenates and returns the user's first and last name."""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_completed_profile(self) -> bool:
        """
        Checks if essential profile information is completed.

        Returns:
            bool: True if all required profile fields are populated, False otherwise.
        """
        return all([self.first_name, self.last_name, self.email, self.phone_number])

    def set_reset_password_token(self) -> str:
        """
        Generates and sets a password reset token for the user.

        Returns:
            str: The generated reset password token.
        """
        self.reset_password_token = generate_reset_password_token()
        self.save()
        return self.reset_password_token

    def verify_email(self) -> None:
        """Marks the user's email as verified and saves the change."""
        self.is_verified_email = True
        self.save()

    def verify_phone_number(self) -> None:
        """Marks the user's phone number as verified and saves the change."""
        self.is_verified_phone_number = True
        self.save()
