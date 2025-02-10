# apps/account/serializers/registration_serializers.py

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from ..models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer validates and creates a new user instance.
    """

    def validate_password(self, value: str) -> str:
        """
        Validates the provided password using Django's password validation.

        Args:
            value (str): The password to validate.

        Returns:
            str: The validated password.
        """
        return validate_password(value)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_number", "username", "password")
        read_only_fields = ("id",)


class RegisterConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming user registration.

    This serializer validates the email and the confirmation code during registration confirmation.
    """

    email = serializers.EmailField()
    code = serializers.CharField()
