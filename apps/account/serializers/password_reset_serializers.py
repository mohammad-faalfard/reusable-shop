# apps/account/serializers/password_reset_serializers.py

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class ResetPasswordRequestSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.

    This serializer validates the email provided for password reset requests.
    """

    email = serializers.CharField()


class ResetPasswordConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming the password reset process.

    This serializer validates the email and confirmation code during the password reset confirmation.
    """

    email = serializers.CharField()
    code = serializers.CharField()


class ResetPasswordSetPasswordSerializer(serializers.Serializer):
    """
    Serializer for setting a new password during the password reset process.

    This serializer validates the provided token and password.
    """

    token = serializers.CharField()
    password = serializers.CharField(validators=[validate_password])
