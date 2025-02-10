from django.db import models
from django.utils.translation import gettext_lazy as _

from core import choice
from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class OrderStatus(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Represents the status of an order, including the status type, timestamp,
    and estimated delivery time.

    Fields:
        is_active (bool): Determines if the record is active.
        order (ForeignKey): The order related to this status.
        type (PositiveSmallIntegerField): The type of order status, defined by choices in `OrderStatusChoices`.
        timestamp (DateTimeField): The timestamp when this status was created.
        estimated_time (DateField): The estimated delivery time, if applicable.
        created_at (datetime): The timestamp when the record was created.
        updated_at (datetime): The timestamp when the record was last updated.
        updated_by (int): ID of the user who last updated the record.
        created_by (int): ID of the user who created the record.

    Related OrderStatusChoices:
        PAYMENT_WAITING (0): Payment waiting.
        ORDER_PLACED (1): Order placed.
        PRODUCT_PACKAGING (2): Product packaging.
        READY_FOR_SHIPMENT (3): Ready for shipment.
        ON_THE_WAY (4): On the way.
        DROPPED_IN_DELIVERY (5): Dropped in the delivery station.
        DELIVERED (6): Delivered.
        CANCELED (7): Canceled.
    """

    order = models.ForeignKey(
        "order.Order",
        on_delete=models.PROTECT,
        related_name="order_statuses",
        verbose_name=_("Order"),
        help_text=_("The order related to this status"),
    )
    type = models.PositiveSmallIntegerField(
        choices=choice.ORDER_STATUSES,
        verbose_name=_("Order Status Type"),
        help_text=_("The type of order status"),
    )
    timestamp = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Timestamp"),
        editable=True,
    )
    estimated_time = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Estimated Delivery Time"),
    )

    def __str__(self):
        return _("Order #{} Status {}").format(self.order.id, self.get_type_display())

    class Meta:
        verbose_name = _("Order Status")
        verbose_name_plural = _("Order Statuses")
        ordering = ["-created_at"]
