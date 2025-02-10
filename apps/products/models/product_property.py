from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, PriorityMixin, UpdatedByMixin

from .product import Product


class ProductProperty(BaseModel, CreatedByMixin, PriorityMixin, UpdatedByMixin):
    """
    Model representing additional attributes for a product, such as color, size, or weight.

    Attributes:
        is_active (bool): Status of the property, determines if it is visible.
        priority (int): Determines the order in which properties are displayed.
        title (str): Name of the property, e.g., "Color" or "Weight".
        value (int): Value of the property, e.g., "Red" or "500g".
        created_at (datetime): The date and time when the property was created.
        updated_at (datetime): The date and time when the property was last updated.
        updated_by (int): ID of the user who last updated the property.
        created_by (int): ID of the user who created the property.
        product (Product): Foreign key linking this property to a specific product.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )
    value = models.CharField(
        max_length=100,
        verbose_name=_("Value"),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_properties",
        verbose_name=_("Product"),
    )

    class Meta:
        verbose_name = _("Product Property")
        verbose_name_plural = _("Product Properties")
        unique_together = (
            "product",
            "title",
            "value",
        )  # Enforcing that each combination of title and value is unique for a product

    def __str__(self):
        return f"{self.title}: {self.value}"
