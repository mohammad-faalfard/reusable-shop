# apps/promotions/queries.py
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.account.models import User
from core import choice

from .models import Coupon, CouponConsume


def coupon_validate(user: User, coupon: Coupon, cart_total_price: float) -> Coupon | None:
    """
    Validate if the given coupon code is usable for the user, considering timezones,
    start date, and expiry date.

    Args:
        user (User): The user attempting to use the coupon.
        coupon_code (str): The code of the coupon to validate.
        cart_total_price (float): The total price of the user's cart.

    Returns:
        Coupon | None: Returns the valid coupon instance if valid, None otherwise.

    Raises:
        ValidationError: If the coupon is invalid, expired, not yet valid,
                          already used, no longer active, or if the cart total price is insufficient.
    """

    if not isinstance(coupon, Coupon):
        raise ValidationError(_("Invalid coupon code."))

    # Use timezone-aware current time for comparison
    current_time = timezone.now()
    # Check if the coupon has an expiry date and if it's within the valid time window (valid_from to valid_until)
    if coupon.valid_until and current_time > coupon.valid_until:
        raise ValidationError(_("This coupon has expired."))

    # If either valid_from or valid_until is not set, skip that validation.
    if not coupon.valid_from and not coupon.valid_until:
        # If no date constraints, it means the coupon is valid indefinitely.
        pass
    elif not coupon.valid_from:
        # If no valid_from date, assume it can be used anytime before valid_until
        pass
    elif not coupon.valid_until:
        # If no valid_until date, assume it can be used anytime after valid_from
        pass
    # Check if the coupon is within the valid time window (valid_from to valid_until)
    if coupon.valid_from and current_time < coupon.valid_from:
        raise ValidationError(_("This coupon is not yet valid."))

    if coupon.valid_until and current_time > coupon.valid_until:
        raise ValidationError(_("This coupon has expired."))

    # Check if the coupon has reached its usage limit
    if coupon.total and CouponConsume.objects.filter(coupon=coupon).count() >= coupon.total:
        raise ValidationError(_("This coupon has reached its usage limit."))

    # Ensure the user hasn't already used this coupon
    if CouponConsume.objects.filter(user=user, coupon=coupon).exists():
        raise ValidationError(_("You have already used this coupon."))

    # Check if the coupon is active
    if not coupon.is_active:
        raise ValidationError(_("This coupon is no longer active."))

    # Check if the coupon has a minimum cart value
    if coupon.min_cart is not None and cart_total_price < coupon.min_cart:
        raise ValidationError(_("Your cart total price must be at least {coupon.min_cart} to use this coupon."))

    return coupon


def calculate_cart_discount(cart_value: float, coupon: Coupon) -> float:
    """
    Calculate the discount to be applied to a cart based on the provided coupon.

    The discount can either be a fixed amount or a percentage of the cart value.
    If the coupon type is a percentage, the discount is capped by the maximum discount limit.

    Args:
        cart_value (float): The total value of the user's cart.
        coupon (Coupon): The coupon to apply to the cart. It can either provide a fixed amount discount or a percentage discount.

    Returns:
        float: The final price after applying the discount.

    Notes:
        - If the coupon type is a fixed amount (COUPON_TYPE_AMOUNT), the discount is simply the coupon's amount.
        - If the coupon type is a percentage (COUPON_TYPE_PERCENT), the discount is calculated based on the cart value, but it will never exceed the coupon's `max_discount_total`.
    """
    if coupon.type == choice.COUPON_TYPE_AMOUNT:
        # Apply fixed discount
        discount = coupon.amount
    elif coupon.type == choice.COUPON_TYPE_PERCENT:
        # Apply percentage discount, but ensure it doesn't exceed the max discount total
        discount = (cart_value * coupon.amount) / 100
        coupon.max_discount_total = coupon.max_discount_total or float("inf")
        discount = min(discount, coupon.max_discount_total)
    else:
        discount = 0.0

    # Calculate the discounted price
    discounted_price = cart_value - discount

    return discounted_price


def get_coupon_by_id(coupon_id: int) -> Coupon | None:
    """
    Retrieve a Coupon instance by its ID.

    Args:
        coupon_id (int): The ID of the coupon to retrieve.

    Returns:
        Coupon | None: The Coupon instance if found, otherwise None.
    """
    try:
        return Coupon.objects.get(id=coupon_id)
    except Coupon.DoesNotExist:
        return None


def get_coupon_by_code(coupon_code: str) -> Coupon | None:
    """
    Retrieve a Coupon instance by its ID.

    Args:
        coupon_id (int): The ID of the coupon to retrieve.

    Returns:
        Coupon | None: The Coupon instance if found, otherwise None.
    """
    try:
        return Coupon.objects.get(code=coupon_code)
    except Coupon.DoesNotExist:
        return None


def consume_coupon(user, total_price_order, coupon: Coupon) -> bool:
    """
    Consume a coupon by setting its `consumed` field to True.
    Args:
        coupon_id (int): The ID of the coupon to consume.
    Returns:
        bool: True if the coupon was successfully consumed, False otherwise.
    """
    coupon_validate(
        user=user,
        cart_total_price=total_price_order,
        coupon=coupon,
    )
    obj = CouponConsume.objects.create(user=user, coupon=coupon)
    return obj
