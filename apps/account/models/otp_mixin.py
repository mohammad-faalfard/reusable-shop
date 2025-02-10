# apps/account/models/otp_mixin.py

import string

from django.core.cache import cache
from django.utils.crypto import get_random_string


class OTPMixin:
    """
    OTP Mixin providing functionality for generating and validating one-time passwords (OTPs).

    Attributes:
        OTP_LENGTH (int): Length of the generated OTP.
        OTP_EXPIRE_TIME (int): Time in seconds for OTP expiration in cache.

    Methods:
        set_otp: Generates and stores a random OTP in the cache.
        get_otp: Retrieves the OTP from the cache if it exists.
        check_otp: Validates a provided OTP against the cached OTP.
    """

    OTP_LENGTH: int = 6
    OTP_EXPIRE_TIME: int = 120  # OTP expiration time in seconds

    @property
    def __key(self) -> str:
        """Returns a unique cache key for the OTP using the user's primary key."""
        return f"otp_{self.pk}"

    def set_otp(self) -> str:
        """
        Generates and caches a numeric OTP of specified length.

        Returns:
            str: The generated OTP.
        """
        otp = get_random_string(length=self.OTP_LENGTH, allowed_chars=string.digits)
        cache.set(self.__key, otp, self.OTP_EXPIRE_TIME)
        return otp

    def check_otp(self, value: str) -> bool:
        """
        Validates the provided OTP against the cached OTP.

        Args:
            value (str): The OTP to check.

        Returns:
            bool: True if the OTP is valid, False otherwise.
        """
        return self.get_otp() == value

    def get_otp(self) -> str | None:
        """
        Retrieves the cached OTP if it exists.

        Returns:
            str | None: The OTP if it exists, None otherwise.
        """
        return cache.get(self.__key)
