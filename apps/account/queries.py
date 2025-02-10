from django.db.models import Q

from .models import Address, User


def get_user_address(user) -> Address | None:
    """
    Fetches the user's single address (assuming there's only one address per user).
    Returns None if no address is found.
    """
    return Address.objects.filter(user=user).first()


def get_user_by_email_or_username(identifier: str) -> User | None:
    """
    Retrieves a user by email address or username.

    Args:
        identifier (str): The email or username to search for.

    Returns:
        User or None: Returns the user object if found, otherwise None.
    """
    return User.objects.filter(Q(email=identifier) | Q(username=identifier)).first()
