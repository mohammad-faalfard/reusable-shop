# apps/account/serializers/user_serializers.py

from rest_framework import serializers

from apps.wallet.serializers import WalletSerializer

from ..models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user data representation.

    This serializer is used to display user information, including the wallet.
    """

    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "phone_number", "username", "wallet")
        read_only_fields = ("id", "wallet")
