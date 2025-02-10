from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core import choice
from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class Coupon(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Represents a discount coupon that can be applied to a user's cart to reduce the total cost.

    A coupon can be either a fixed amount or a percentage-based discount. It can have a
    specific validity period, usage limits, and can be restricted to specific users.
    Coupons can also be subject to a minimum cart value and a maximum discount limit
    (for percentage discounts).

    Attributes:
        title (str): A descriptive name for the coupon, typically shown to the user.
        code (str): A unique code used by users to apply the coupon.
        valid_from (datetime): The start date and time when the coupon becomes valid.
        valid_until (datetime): The expiration date and time of the coupon.
        total (int): The maximum number of times this coupon can be used across all users.
        users (ManyToManyField): Users eligible to use the coupon. If empty, the coupon is available to all users.
        type (PositiveSmallIntegerField): The type of discount: either a fixed amount or a percentage.
        min_cart (float): The minimum cart value required to apply this coupon.
        amount (float): The actual discount amount for fixed amount discounts.
        max_discount_total (float): The maximum discount amount for percentage-based discounts.

    Methods:
        __str__(self): Returns the coupon code as the string representation of the coupon.
        clean(self): Validates that `valid_from` is not later than `valid_until`, and checks
                    the appropriateness of `amount` and `max_discount_total` fields for different coupon types.
        fixed_discount(self): Returns the fixed discount amount for a fixed discount coupon.
        percentage_discount(self): Returns a function that calculates the percentage discount based on the cart value,
                                    capped by the `max_discount_total` for percentage-based coupons.
        calculate_discount(self, cart_value): Calculates the discount to be applied to the cart based on the coupon type
                                               (fixed or percentage).

    Meta:
        verbose_name (str): The human-readable singular name for the model in the admin interface.
        verbose_name_plural (str): The human-readable plural name for the model in the admin interface.
        ordering (list): Default ordering of coupon records, sorted by creation date in descending order.
    """

    title = models.CharField(max_length=100, verbose_name=_("Title"))
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Code"),
        help_text=_("Unique code to apply this coupon."),
    )
    valid_from = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Valid From"),
        help_text=_("The start date and time for coupon validity."),
    )
    valid_until = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Valid Until"),
        help_text=_("The end date and time for coupon validity."),
    )
    total = models.PositiveIntegerField(
        verbose_name=_("Total Uses"),
        help_text=_("Maximum number of times this coupon can be used."),
        validators=[MinValueValidator(1)],
    )
    users = models.ManyToManyField(
        "account.User",
        related_name="coupons",
        blank=True,
        verbose_name=_("Eligible Users"),
        help_text=_("Users eligible to use this coupon."),
    )
    type = models.PositiveSmallIntegerField(
        choices=choice.COUPON_TYPES,
        db_index=True,
        verbose_name=_("Discount Type"),
        help_text=_("Type of discount: percentage or fixed amount."),
    )
    min_cart = models.FloatField(
        verbose_name=_("Minimum Cart Value"),
        help_text=_("Minimum cart value required to apply this coupon."),
        validators=[MinValueValidator(0.0)],
    )
    amount = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Discount Amount"),
        help_text=_("The actual discount amount applied to the cart (fixed or percentage)."),
        validators=[MinValueValidator(0.0)],
    )
    max_discount_total = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_("Maximum Discount Total"),
        help_text=_("Maximum discount amount for a cart when the coupon type is percentage."),
        validators=[MinValueValidator(0.0)],
    )

    def __str__(self):
        """
        Returns the coupon code as the string representation of the coupon.

        Returns:
            str: The unique code for the coupon.
        """
        return self.code

    def clean(self):
        """
        Validates the fields of the Coupon model before saving:
        - Ensures `valid_from` is not later than `valid_until`.
        - Ensures that if the coupon type is percentage, `amount` is between 0 and 100.

        Raises:
            ValidationError: If any of the validation checks fail.
        """
        if self.valid_from and self.valid_until and self.valid_from > self.valid_until:
            raise ValidationError(_("The valid_from date cannot be later than the valid_until date."))

        # Validate percentage discount range in a single if condition
        if self.type == choice.COUPON_TYPE_PERCENT and (self.amount is None or self.amount < 0 or self.amount > 100):
            raise ValidationError(_("For percentage discounts, the amount must be between 0 and 100."))

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")
        ordering = ["-created_at"]
