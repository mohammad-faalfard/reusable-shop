import contextlib

from django.db.models import Q
from django.db.models.query import QuerySet
from django.forms import ValidationError

from apps.account.models import User
from apps.products.models import Product
from apps.products.queries import calculate_product_discount
from apps.promotions.models.coupon import Coupon
from apps.promotions.queries import calculate_cart_discount, coupon_validate

from .models import Cart, CartItem


def create_cart(user: User = None, session_id: str = None) -> Cart:
    """
    Creates a new cart for the user or session.

    Args:
        user (User | None): The user to associate the cart with, or None for session-based cart.
        session_id (str | None): The session ID to associate the cart with, or None for user-based cart.

    Returns:
        Cart: The newly created cart.
    """
    if user and user.is_anonymous:
        user = None
    print(user, session_id)
    cart = Cart.objects.create(
        user=user,
        session_id=session_id,
    )
    return cart


def get_total_inside_cart(product: object, user=None, session_id: str = None) -> int:
    """
    Retrieves the total quantity of a specific product in the user's cart.

    Args:
        product (Product): The product to check in the cart.
        user (User | None): The user associated with the cart, or None for session-based cart.
        session_id (str | None): The session ID associated with the cart, or None for user-based cart.

    Returns:
        int: The quantity of the product in the cart, or 0 if not found.
    """
    cart = get_cart(user, session_id)
    if not cart:
        return 0

    item = cart.items.filter(product=product).first()
    quantity = item.quantity if item else 0
    return quantity


def add_or_update_cart_item(product: object, quantity: int = 1, cart: Cart = None) -> CartItem:
    """
    Adds a product to the cart or updates its quantity if it already exists.

    Args:
        product (object): The product to add or update in the cart.
        quantity (int): The quantity of the product to add to the cart. Defaults to 1.
        cart (Cart): The cart to which the product belongs. This is required.

    Returns:
        CartItem: The updated or newly created cart item.
    """
    available_quantity = min(quantity, product.stock)
    if not available_quantity:
        return None

    product_item, new_item = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={"quantity": quantity},
    )
    if not new_item:
        product_item.quantity = quantity
        product_item.save()

    return product_item


def remove_from_cart_item(product: object, cart: Cart = None) -> bool:
    """
    Removes a product from the cart.

    Args:
        product (object): The product to remove from the cart.
        cart (Cart): The cart from which to remove the product.

    Returns:
        bool: True if the item was removed, False otherwise.
    """
    product_item = cart.items.filter(
        product=product,
    ).first()
    if product_item:
        product_item.delete()

    return bool(product_item)


def add_or_update_cart_items(cart: Cart, products: list[tuple[object, int]]) -> QuerySet[CartItem]:
    """
    Adds or updates multiple products in the cart.

    Args:
        cart (Cart): The cart to which the products belong.
        products (list of tuple): A list of tuples, each containing a product and its quantity.

    Returns:
        QuerySet[CartItem]: A queryset of the created or updated CartItem instances.
    """
    cart_items = [add_or_update_cart_item(cart, product, quantity) for (product, quantity) in products]
    cart_items = filter(None, cart_items)
    cart_items = CartItem.objects.bulk_create(cart_items)
    return cart_items


def get_cart(user: User = None, session_id: str = None) -> Cart | None:
    """
    Retrieves the user's cart, either by user or session ID. Creates a new cart if none is found.

    Args:
        user (User | None): The user whose cart to retrieve, or None for session-based cart.
        session_id (str | None): The session ID associated with the cart, or None for user-based cart.

    Returns:
        Cart | None: The user's cart, or None if no cart exists and creation fails.
    """
    if user and user.is_anonymous:
        user = None

    cart = (
        Cart.objects.filter(
            Q(user=user) | Q(session_id=session_id),
        )
        .order_by("-updated_at")
        .first()
    )
    print(user, session_id)
    if not cart:
        cart = create_cart(user, session_id)
    return cart


def get_cart_item(cart: Cart, product: Product) -> QuerySet[CartItem]:
    """
    Retrieves item in the cart.

    Args:
        cart (Cart): The cart from which to retrieve the items.
        product (Product): The product which want to retrieve.

    Returns:
        QuerySet[CartItem]: A queryset of all cart items.
    """
    return cart.items.filter(product=product).first()


def get_cart_items(cart: Cart) -> QuerySet[CartItem]:
    """
    Retrieves all items in the cart.

    Args:
        cart (Cart): The cart from which to retrieve the items.

    Returns:
        QuerySet[CartItem]: A queryset of all cart items.
    """
    return cart.items.all()


def update_cart_items_quantities(cart: Cart) -> None:
    """
    Updates the quantity of each item in the cart based on the current stock.
    Returns: None
    """
    updated_items = []
    for item in cart.items.all():
        if item.product.stock >= item.quantity:
            continue
        else:
            item.quantity = item.product.stock
            updated_items.append(item)
    CartItem.objects.bulk_update(updated_items, ["quantity"])


def get_cart_item_count(cart) -> int:
    """
    Retrieves the total number of items in the cart.

    Args:
        cart (Cart): The cart to retrieve item count for.

    Returns:
        int: The total quantity of all items in the cart.
    """
    return sum(item.quantity for item in cart.items.all())


def get_cart_items_total_price(cart: Cart, coupon: Coupon | None = None) -> dict[str, float]:
    """
    Calculates the total price of items in the cart, optionally applying a discount from a coupon.

    Args:
        cart (Cart): The user's cart containing the items.
        coupon (str | None): The coupon code to apply (if any), or None for no discount.

    Returns:
        dict: A dictionary containing the total price breakdown:
            - product_total_price: Total price of products before any discounts.
            - coupon_total_discount: Total discount applied by the coupon (if any).
            - product_total_discount: Total discount applied to the products.
            - total_price: Final total price after applying all discounts.
    """
    # Retrieve cart items and calculate individual product discounts
    items = get_cart_items(cart).select_related("product").prefetch_related("product__discounts", "product__offers")

    # Calculate original product prices and discounts
    product_total_price: float = sum(item.product.price * item.quantity for item in items)
    product_total_discount: float = sum(
        ((item.product.price * item.quantity) - calculate_product_discount(item.product, item.quantity)[1]) for item in items
    )
    final_price_of_products: list[float] = [calculate_product_discount(item.product, item.quantity)[1] for item in items]
    sum_final_price_of_products: float = sum(final_price_of_products)

    # Initialize coupon discount and validated coupon
    coupon_total_discount: float = 0.0
    validated_coupon = None

    if not coupon:
        ...
    else:
        with contextlib.suppress(ValidationError):
            validated_coupon = coupon_validate(cart.user, coupon, sum_final_price_of_products)
        if validated_coupon:
            coupon_total_discount = sum_final_price_of_products - calculate_cart_discount(
                sum_final_price_of_products, validated_coupon
            )
            sum_final_price_of_products = calculate_cart_discount(sum_final_price_of_products, validated_coupon)

    return {
        "product_total_price": product_total_price,
        "coupon_total_discount": coupon_total_discount,
        "product_total_discount": product_total_discount,
        "total_price": sum_final_price_of_products,
        "coupon_id": validated_coupon.id if validated_coupon else None,
    }
