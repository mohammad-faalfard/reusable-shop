from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class CustomAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows login using username, email, or phone number.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        # Check if username or email or phone number exists
        user = User.objects.filter(Q(username=username) | Q(email=username) | Q(phone_number=username)).first()

        # If a user is found and password matches
        if user and user.check_password(password):
            return user
        return None
