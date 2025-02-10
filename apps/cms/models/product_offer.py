from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class ProductOffer(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Model representing a promotional offer for products.

    Attributes:
        is_active (bool): Indicates whether the offer is active.
        title (str): The title of the offer.
        active_from (datetime): The start date and time of the offer's validity.
        active_until (datetime): The end date and time of the offer's validity.
        created_at (datetime): Timestamp of when the offer was created.
        updated_at (datetime): Timestamp of the last update to the offer.
        updated_by (int): ID of the user who last updated the offer.
        created_by (int): ID of the user who created the offer.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )
    active_from = models.DateTimeField(
        verbose_name=_("Active From"),
        db_index=True,
    )
    active_until = models.DateTimeField(
        verbose_name=_("Active Until"),
        db_index=True,
    )

    class Meta:
        verbose_name = _("Product Offer")
        verbose_name_plural = _("Product Offers")

    def __str__(self):
        return self.title


class ProductOfferItem(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Model representing an individual item within a product offer.

    Attributes:
        is_active (bool): Indicates whether the offer item is active.
        product_offer (int): ID of the product offer associated with the offer item.
        product (int): ID of the product associated with the offer item.
        stock (int): Available stock for this product within the offer.
        discount (float): Discount percentage for the product within the offer.
        created_at (datetime): Timestamp of when the item was created.
        updated_at (datetime): Timestamp of the last update to the item.
        updated_by (int): ID of the user who last updated the item.
        created_by (int): ID of the user who created the item.
    Constraints:
        - Ensures each product only appears once in an offer, can be extended in the future.
    """

    product_offer = models.ForeignKey(
        "cms.ProductOffer",
        related_name="offer_items",
        on_delete=models.CASCADE,
        verbose_name=_("Product Offer"),
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        db_index=True,
        related_name="offers",
    )
    stock = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Stock"),
        db_index=True,
    )
    sold_stock = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Sold Stock"),
        db_index=True,
    )
    discount = models.FloatField(
        verbose_name=_("Discount"),
        validators=[MinValueValidator(0)],
        help_text=_("Percent"),
        db_index=True,
    )

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = _("Product Offer Item")
        verbose_name_plural = _("Product Offer Items")
        constraints = [
            # Enforces uniqueness for each product in the offer.
            # Can be modified to include additional fields or business logic in the future.
            models.UniqueConstraint(fields=["product"], name="unique_product_offer_item"),
        ]
