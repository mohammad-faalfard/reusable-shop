from rest_framework.serializers import ModelSerializer

from .models import Wallet, WalletTransaction


class WalletSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("current_balance",)
        read_only_fields = fields


class WalletTransactionSerializer(ModelSerializer):
    class Meta:
        model = WalletTransaction
        fields = (
            "id",
            "value",
            "log",
            "total_balance",
        )
