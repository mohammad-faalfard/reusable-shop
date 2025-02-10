# apps/account/serializers/auth_serializers.py

from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.

    This serializer validates user credentials during the login process.
    """

    email = serializers.EmailField()
    password = serializers.CharField()


class RequestOtpSerializer(serializers.Serializer):
    """
    Serializer for requesting an OTP (One-Time Password).

    This serializer validates the email provided for OTP requests.
    """

    email = serializers.EmailField()
