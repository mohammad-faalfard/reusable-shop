from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class OrderShipment(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Represents the shipment details of an order, including shipment type, price, and shipping date.

    Fields:
        is_active (bool): Determines if the record is active.
        order (ForeignKey): The order associated with this shipment.
        shipment_type (ForeignKey): The type of shipment used, linked to the `ShipmentType` model.
        shipping_date (DateTimeField): The date when the shipment was made.
        shipment_price (FloatField): The price of the shipment.
        created_at (datetime): The timestamp when the record was created.
        updated_at (datetime): The timestamp when the record was last updated.
        updated_by (int): ID of the user who last updated the record.
        created_by (int): ID of the user who created the record.
    """

    order = models.ForeignKey(
        "order.Order",
        on_delete=models.PROTECT,
        related_name="order_shipments",
        verbose_name=_("Order"),
        help_text=_("The order associated with this shipment"),
    )
    shipment_type = models.ForeignKey(
        "shipments.ShipmentType",
        on_delete=models.PROTECT,
        verbose_name=_("Shipment Type"),
    )
    shipping_date = models.DateTimeField(
        verbose_name=_("Shipping Date"),
        help_text=_("The date when the shipment was made"),
    )
    shipment_price = models.FloatField(
        verbose_name=_("Shipment Price"),
    )

    def __str__(self):
        """
        Return a string representation of the shipment, including the order ID and shipment type.
        """
        return _("Shipment #{} for Order #{}").format(self.id, self.order.id)

    class Meta:
        verbose_name = _("Order Shipment")
        verbose_name_plural = _("Order Shipments")
        ordering = ["-created_at"]
