from __future__ import unicode_literals

from django.conf import settings
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel

from .errors import InsufficientBalance

# We'll be using BigIntegerField by default instead
# of DecimalField for simplicity. This can be configured
# though by setting `WALLET_CURRENCY_STORE_FIELD` in your
# `settings.py`.
CURRENCY_STORE_FIELD = getattr(settings, "WALLET_CURRENCY_STORE_FIELD", models.BigIntegerField)


class Wallet(BaseModel):
    # We should reference to the AUTH_USER_MODEL so that
    # when this module is used and a different User is used,
    # this would still work out of the box.
    # like a cache to the wallet's balance as well.
    title = models.CharField(_("title"), max_length=50, null=False, blank=True, default=True)
    current_balance = CURRENCY_STORE_FIELD(default=0, verbose_name=_("current balance"))

    class Meta:
        verbose_name = _("wallet")
        verbose_name_plural = _("wallets")

    def __str__(self) -> str:
        return f"{self.title}: {self.current_balance}"

    def _deposit(self, value):
        """Deposits a value to the wallet.

        Also creates a new transaction with the deposit
        value.
        """
        self.transaction_set.create(value=value, total_balance=self.current_balance + value)
        self.current_balance += value
        self.save()

    def _withdraw(self, value):
        """Withdraw's a value from the wallet.

        Also creates a new transaction with the withdraw
        value.

        Should the withdrawn amount is greater than the
        balance this wallet currently has, it raises an
        :mod:`InsufficientBalance` error. This exception
        inherits from :mod:`django.db.IntegrityError`. So
        that it automatically rolls-back during a
        transaction lifecycle.
        """
        if value > self.current_balance:
            raise InsufficientBalance("This wallet has insufficient balance.")

        self.transaction_set.create(value=-value, total_balance=self.current_balance - value)
        self.current_balance -= value
        self.save()

    @classmethod
    def transfer(cls, src_id, dst_id, value):
        """Transfers an value to another wallet.

        Uses `deposit` and `withdraw` internally.
        """
        with transaction.atomic():
            src_wallet = cls.objects.select_for_update().get(id=src_id)
            dst_wallet = cls.objects.select_for_update().get(id=dst_id)
            src_wallet._withdraw(value=value)
            dst_wallet._deposit(value=value)

    @classmethod
    def deposit(cls, id, value):
        with transaction.atomic():
            wallet = cls.objects.select_for_update().get(id=id)
            wallet._deposit(value=value)

    @classmethod
    def withdraw(cls, id, value):
        with transaction.atomic():
            wallet = cls.objects.select_for_update().get(id=id)
            wallet._withdraw(value=value)


class WalletTransaction(BaseModel):
    # The wallet that holds this transaction.
    wallet = models.ForeignKey(verbose_name=_("wallet"), to="wallet.Wallet", on_delete=models.CASCADE)

    # The value of this transaction.
    value = CURRENCY_STORE_FIELD(default=0, verbose_name=_("value"))
    log = models.CharField(_("log"), max_length=50, blank=True, null=False, default="")

    # The value of the wallet at the time of this
    # transaction. Useful for displaying transaction
    # history.
    total_balance = CURRENCY_STORE_FIELD(default=0, verbose_name=_("total balance"))

    class Meta:
        verbose_name = _("wallet transaction")
        verbose_name_plural = _("wallet transactions")

    def __str__(self) -> str:
        return f"{self.wallet_id}: {self.value} -> {self.total_balance}"
