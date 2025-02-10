from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle.decorators import hook
from django_lifecycle.hooks import AFTER_SAVE

from core import choice
from core.models import BaseModel, CreatedByMixin, PriorityMixin, UpdatedByMixin


class ProductDiscount(BaseModel, CreatedByMixin, PriorityMixin, UpdatedByMixin):
    """
    Model representing a discount that can be applied to products. Discounts
    can be percentage-based or fixed-amount reductions.

    Attributes:
        is_active (bool): Status of the discount, determines if it is active.
        title (str): The name of the discount.
        type (str): Type of the discount ('percent'(0) or 'amount'(1)).
        amount (float): The discount value, either a percentage or fixed amount.
        active_from (datetime): Start date and time for the discount validity.
        active_until (datetime): End date and time for the discount validity.
        created_at (datetime): The date and time when the discount was created.
        updated_at (datetime): The date and time when the discount was last updated.
        updated_by (int): ID of the user who last updated the discount.
        created_by (int): ID of the user who created the discount.
    """

    product = models.ForeignKey(
        to="products.product",
        verbose_name=_("Product"),
        on_delete=models.CASCADE,
        related_name="discounts",
    )

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )
    type = models.PositiveSmallIntegerField(
        choices=choice.DISCOUNT_TYPES,
        verbose_name=_("Type"),
    )
    amount = models.FloatField(
        verbose_name=_("Amount"),
        validators=[MinValueValidator(0)],
    )  # Ensures amount is greater than or equal to 0
    active_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Active From"),
    )
    active_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Active Until"),
    )

    class Meta:
        verbose_name = _("Product Discount")
        verbose_name_plural = _("Product Discounts")

    def __str__(self):
        return self.title

    @hook(
        AFTER_SAVE,
    )
    def handel_active_discount(self):
        if self.is_active:
            self.product.discounts.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)

    def clean(self):
        # Custom validation for the amount based on discount type
        #  - For percentage discounts (DiscountType.PERCENT), the amount must be between 0 and 100.
        if self.type == choice.DISCOUNT_TYPE_PERCENT and (self.amount < 0 or self.amount > 100):
            raise ValidationError(_("For percentage discounts, amount must be between 0 and 100."))
