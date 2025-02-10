from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core import choice
from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class Order(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Represents an order placed by a user, including details about the shipping address,
    applied coupon, order notes, and pricing (product total, discounts, and final price).

    Fields:
        is_active (bool): Determines if the record is active.
        user (ForeignKey): The user who placed the order.
        address (ForeignKey): The shipping address for the order.
        coupon (ForeignKey): The coupon applied to the order (optional).
        note (TextField): Special instructions for the order, up to 1000 characters.
        product_total_price (FloatField): The total price of all products in the order.
        coupon_total_discount (FloatField): The discount applied via a coupon.
        product_total_discount (FloatField): The total discount applied to products.
        total_price (FloatField): The final total price after applying all discounts.
        created_at (datetime): The timestamp when the record was created.
        updated_at (datetime): The timestamp when the record was last updated.
        updated_by (int): ID of the user who last updated the record.
        created_by (int): ID of the user who created the record.
    """

    user = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("User"),
        help_text=_("The user who placed the order"),
    )
    address = models.ForeignKey(
        "account.Address",
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("Shipping Address"),
        help_text=_("The shipping address for the order"),
    )
    coupon = models.ForeignKey(
        "promotions.Coupon",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="orders",
        verbose_name=_("Coupon"),
        help_text=_("The coupon applied to the order"),
    )
    note = models.TextField(
        verbose_name=_("Order Note"),
        blank=True,
        null=True,
        validators=[MaxLengthValidator(1000)],
        help_text=_("Any special instructions for the order. Maximum 1000 characters"),
    )
    product_total_price = models.FloatField(
        verbose_name=_("Total Product Price"),
        help_text=_("The total price of all products before any discounts."),
    )

    coupon_total_discount = models.FloatField(
        verbose_name=_("Coupon Discount"),
        help_text=_("Total discount applied via coupon. This is the discount from a coupon applied to the order."),
    )

    product_total_discount = models.FloatField(
        verbose_name=_("Product Discount"),
        help_text=_("Total discount applied directly to the products. This does not include coupon discounts."),
    )
    shipment_price = models.FloatField(
        verbose_name=_("Shipment Price"),
        help_text=_("The shipment price"),
        default=0,
    )
    total_price = models.FloatField(
        verbose_name=_("Total Price"),
        help_text=_(
            "The final total price after all discounts (both product and coupon discounts) have been applied and shipment price."
        ),
    )
    current_status = models.PositiveSmallIntegerField(
        choices=choice.ORDER_STATUSES,
        default=choice.ORDER_STATUS_ORDER_PLACED,
        verbose_name=_("Current Order Status"),
        help_text=_("The Current Order Status"),
    )

    def __str__(self):
        return _("Order #{} for {}").format(self.id, self.user)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ["-created_at"]

    def calculate_total_price(self):
        """Calculates the total price of the order."""
        total_price = (self.product_total_discount - self.coupon_total_discount) + self.shipment_price
        total_price = max(total_price, 0)
        return total_price
