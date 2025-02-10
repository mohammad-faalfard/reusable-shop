from django.core.validators import MaxLengthValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core import choice
from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class ShipmentType(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Represents a shipment type in the system.

    Attributes:
        is_active (bool): Indicates if the shipment type is active.
        title (str): The name of the shipment type.
        service_type (int): Identifier for the type of service.
        description (str): A description of the shipment type (max 500 characters).
        logo (int): Reference to the logo of the shipment type.
        price (int): The base price for the shipment type.
        vat (float): The VAT (Value Added Tax) percentage for the shipment type.(0 to 100)
        created_at (datetime): The timestamp when the shipment type was created.
        updated_at (datetime): The timestamp when the shipment type was last updated.
        updated_by (int): ID of the user who last updated the shipment type.
        created_by (int): ID of the user who created the shipment type.
    """

    title = models.CharField(max_length=100, verbose_name=_("Title"))
    service_type = models.IntegerField(
        choices=choice.SHIPMENT_SERVICE_TYPES,
        verbose_name=_("Service Type"),
        help_text=_("Select the type of service for this shipment."),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
        validators=[MaxLengthValidator(500)],
        help_text=_("A detailed description of the shipment type."),
    )
    logo = models.ImageField(
        upload_to="shipment_type_logos/",
        verbose_name=_("Logo"),
        help_text=_("Upload the logo for the shipment type."),
    )
    price = models.IntegerField(
        verbose_name=_("Price"),
        help_text=_("The base price for this shipment type."),
    )
    vat = models.FloatField(
        verbose_name=_("VAT"),
        help_text=_("The VAT (Value Added Tax) percentage for this shipment type."),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],  # Ensuring VAT is between 0 and 100
    )

    class Meta:
        verbose_name = _("Shipment Type")
        verbose_name_plural = _("Shipment Types")

    def __str__(self):
        """
        Returns the string representation of the shipment type.
        """
        return self.title

    def get_total_price(self) -> float:
        """
        Calculates the total price including VAT for this shipment type.
        If VAT is 0, it returns the base price without VAT.

        Returns:
            float: The total price including VAT, or the base price if VAT is 0.
        """
        if self.vat == 0:
            return float(self.price)  # No VAT applied

        return self.price * (1 + self.vat / 100)  # Calculate total price with VAT
