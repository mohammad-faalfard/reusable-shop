from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class OrderItem(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Represents an individual item in an order, including product details, price,
    quantity, and associated discounts.

    Fields:
        is_active (bool): Determines if the record is active.
        user (ForeignKey): The user who placed the order.
        order (ForeignKey): The order to which this item belongs.
        product (ForeignKey): The product included in the order.
        product_title (CharField): The title of the product.
        product_price (FloatField): The price of the product.
        product_discount (FloatField): Discount applied to the product.
        quantity (PositiveIntegerField): The quantity of the product ordered.
        price (FloatField): The final price after applying quantity and discounts.
        created_at (datetime): The timestamp when the record was created.
        updated_at (datetime): The timestamp when the record was last updated.
        updated_by (int): ID of the user who last updated the record.
        created_by (int): ID of the user who created the record.
    """

    user = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name=_("User"),
        help_text=_("The user who placed the order"),
    )
    order = models.ForeignKey(
        "order.Order",
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name=_("Order"),
        help_text=_("The order to which this item belongs"),
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name=_("Product"),
        help_text=_("The product included in the order"),
    )
    product_title = models.CharField(
        max_length=100,
        verbose_name=_("Product Title"),
    )
    product_price = models.FloatField(
        verbose_name=_("Product Price"),
    )
    product_discount = models.FloatField(
        default=0.0,
        verbose_name=_("Product Discount"),
        help_text=_("Discount applied to the product"),
    )
    quantity = models.PositiveIntegerField(
        verbose_name=_("Quantity"),
        help_text=_("The quantity of the product ordered"),
    )
    price = models.FloatField(
        verbose_name=_("Final Price"),
        help_text=_("The final price after quantity and discounts"),
    )

    def __str__(self):
        return _("OrderItem for {} (x{})").format(self.product_title, self.quantity)

    class Meta:
        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")
        ordering = ["-created_at"]
