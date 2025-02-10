from django.contrib import admin
from unfold.admin import TabularInline

from core.admin import BaseModelAdmin

from .models import Wallet, WalletTransaction


class WalletTransactionInline(TabularInline):
    model = WalletTransaction
    extra = 0


@admin.register(Wallet)
class WalletAdmin(BaseModelAdmin):
    list_display = ("title", "current_balance")
    inlines = [WalletTransactionInline]


@admin.register(WalletTransaction)
class WalletTransactionAdmin(BaseModelAdmin):
    list_display = ("wallet", "value", "total_balance", "log")
