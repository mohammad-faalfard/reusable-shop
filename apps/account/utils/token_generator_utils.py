import string

from django.utils.crypto import get_random_string


def generate_reset_password_token():
    """
    Generates a secure random string to be used as a password reset token.

    Returns:
        str: A random string of 50 characters containing letters.
    """
    return get_random_string(50, string.ascii_letters)
