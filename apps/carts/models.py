from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel

User = get_user_model()


class Cart(BaseModel):
    user = models.ForeignKey(
        to=User,
        related_name="carts",
        unique=True,  # Maybe in the future, users will need to have multiple carts at the same time
        verbose_name=_("User"),
        null=True,  # The User object is optional because it may user at first be a guest
        blank=True,
        on_delete=models.CASCADE,
    )
    session_id = models.CharField(
        verbose_name=_("Session ID"),
        db_index=True,
        unique=True,
        blank=True,  # The Session ID is optional because maybe user is signed
        null=True,
        max_length=64,
    )

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        constraints = (
            models.CheckConstraint(
                condition=models.Q(user__isnull=False) | models.Q(session_id__isnull=False),
                name="card_owner",
                violation_error_message=_("Each cart must at least have a user or session ID."),
            ),
        )

    def __str__(self):
        user = self.user or self.session_id or _("Unknown")
        return f"{user}"

    def clear(self):
        """Clears all items from the cart."""
        self.items.all().delete()


class CartItem(BaseModel):
    cart = models.ForeignKey(
        to=Cart,
        verbose_name=_("Cart"),
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        to="products.product",
        related_name="cart_items",
        verbose_name=_("Cart"),
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name=_("Quantity"),
        default=1,
        db_index=True,
        validators=[
            MinValueValidator(
                1,
                message=_("Minimum Quantity Of Product Is 1"),
            )
        ],
    )

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        constraints = [
            # Unique Together Cart + Product
            models.UniqueConstraint(
                name="unique_product_cart",
                fields=[
                    "cart",
                    "product",
                ],
                violation_error_message=_("Duplicate Product Inside The Cart"),
            ),
        ]

    def __str__(self):
        return f"{self.id}"
