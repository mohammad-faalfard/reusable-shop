from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel

from .product import Product


class ProductWishlist(BaseModel):
    """
    Model representing a product added to a user's wishlist.

    Attributes:
        is_active (bool): Status of the wishlist, determines if it is active.
        product (ForeignKey): A reference to the `Product` that is added to the wishlist.
        user (ForeignKey): A reference to the `User` who added the product to their wishlist.
        created_at (datetime): The date and time when the wishlist was created.
        updated_at (datetime): The date and time when the wishlist was last updated.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Product"),
        related_name="product_wish_list",
    )
    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="product_wish_list",
        verbose_name=_("User"),
    )

    class Meta:
        verbose_name = _("Product Wishlist")
        verbose_name_plural = _("Product Wishlists")

    def __str__(self):
        return f"Wishlist - {self.user} - {self.product}"
