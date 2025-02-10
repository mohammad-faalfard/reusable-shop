from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class CouponConsume(BaseModel):
    """
    Model representing the usage record of a coupon by a specific user.

    Attributes:
        user (ForeignKey): The user who used the coupon.
        coupon (ForeignKey): The coupon that was consumed.
    """

    user = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="coupon_consumptions",
        verbose_name=_("User"),
        help_text=_("The user who used the coupon."),
    )
    coupon = models.ForeignKey(
        "Coupon",
        on_delete=models.PROTECT,
        related_name="consumptions",
        verbose_name=_("Coupon"),
        help_text=_("The coupon that was consumed."),
    )

    def __str__(self):
        return f"{self.user} - {self.coupon.code}"

    class Meta:
        verbose_name = _("Coupon Consumption")
        verbose_name_plural = _("Coupon Consumptions")
        ordering = ["-created_at"]
