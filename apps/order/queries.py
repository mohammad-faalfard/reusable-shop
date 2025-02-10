from datetime import datetime, timedelta
from typing import Optional

from django.db import transaction
from django.utils import timezone

from apps.account.models import Address, User
from apps.carts.models import CartItem
from apps.cms.models import ProductOfferItem
from apps.products.models.product import Product
from apps.products.queries import calculate_product_discount
from apps.promotions.models import Coupon
from apps.promotions.queries import consume_coupon
from apps.shipments.models import ShipmentType
from core import choice

# from core import choice
from .models import Order, OrderItem, OrderShipment, OrderStatus


def place_order(
    user: User,
    address: Address,
    coupon: Optional[Coupon],
    note: Optional[str],
    product_total_price: float,
    coupon_total_discount: float,
    product_total_discount: float,
    total_price: float,
    cart_items: list,
    shipment_id: str,
    status_type: int,
    estimated_delivery_time: Optional[str],
) -> Order:
    """
    High-level function to place an order, its items, shipment, and status.
    Ensures that all parts of the order are created in a transaction.
    """
    with transaction.atomic():
        shipment_type = ShipmentType.objects.get(
            id=shipment_id,
        )
        shipment_price = shipment_type.price

        try:
            consume_coupon(user=user, total_price_order=total_price, coupon=coupon)
        except Exception:
            # reset discount coupon if there is an error during coupon consumption
            coupon = None
            total_price += coupon_total_discount
            coupon_total_discount = 0

        # Create the order
        order = _create_order(
            user=user,
            address=address,
            coupon=coupon,
            note=note,
            product_total_price=product_total_price,
            coupon_total_discount=coupon_total_discount,
            product_total_discount=product_total_discount,
            total_price=total_price,
            shipment_price=shipment_price,
        )

        # Create the order items
        _create_order_items(order, cart_items)
        # Create the shipment
        _create_order_shipment(order, shipment_type)
        # Create the order status
        _create_order_status(order, status_type, estimated_delivery_time)
        return order


def _create_order(
    user: User,
    address: Address,
    coupon: Optional[Coupon],
    note: Optional[str],
    product_total_price: float,
    coupon_total_discount: float,
    product_total_discount: float,
    total_price: float,
    shipment_price: float,
) -> Order:
    """
    Creates and saves an order record.
    """
    total_discount = product_total_discount + coupon_total_discount
    total_price = (product_total_price + shipment_price) - total_discount
    total_price = max(total_price, 0)

    order = Order(
        user=user,
        address=address,
        coupon=coupon,
        note=note,
        product_total_price=product_total_price,
        coupon_total_discount=coupon_total_discount,
        product_total_discount=product_total_discount,
        total_price=total_price,
        shipment_price=shipment_price,
    )
    order.save()
    return order


def _create_order_items(order: Order, cart_items: list[CartItem]) -> list[OrderItem]:
    """
    Creates order items based on the provided data.
    """
    order_items = []
    updated_products = []
    updated_offers = []
    for item_data in cart_items:
        obj, product, offers = _create_order_item(order, item_data, commit=False)
        if not obj:
            continue
        order_items.append(obj)
        updated_products.append(product)
        updated_offers.extend(offers)

    OrderItem.objects.bulk_create(order_items)
    Product.objects.bulk_update(updated_products, fields=["stock"])
    ProductOfferItem.objects.bulk_update(updated_offers, ["sold_stock"])


def _create_order_item(order: Order, item: CartItem, commit: bool = True) -> tuple[OrderItem, Product, list[ProductOfferItem]]:
    """
    Creates a single order item for the given order.
    """
    available_quantity = min(item.quantity, item.product.stock)
    if not available_quantity:
        return None, item.product

    _, total_price, product_price_with_discount = calculate_product_discount(item.product, available_quantity)

    # Ensure accurate discount per unit
    unit_discount = total_price / available_quantity

    obj = OrderItem(
        order=order,
        user=order.user,
        product=item.product,
        product_title=item.product.title,
        product_price=item.product.price,
        product_discount=unit_discount,
        quantity=available_quantity,
        price=total_price,
    )
    # Update Stock and Save the Product
    # TODO: Update Offer Sold Stock Quantity in Offer Table
    product = item.product
    product.stock -= available_quantity
    active_offers = product.offers.filter(is_active=True, product_offer__is_active=True)
    updated_offers = []

    # Calculate the offer updates, but do not commit yet
    for offer in active_offers:
        available_quantity_offer = offer.stock - offer.sold_stock
        offer.sold_stock += min(available_quantity_offer, available_quantity)
        updated_offers.append(offer)

    if commit:
        obj.save()
        product.save()
        ProductOfferItem.objects.bulk_update(updated_offers, ["sold_stock"])
    return obj, product, updated_offers


def _create_order_shipment(order: Order, shipment_type: ShipmentType) -> None:
    """
    Creates the shipment for the given order based on the provided shipment data.
    """

    shipping_date = timezone.now() + timedelta(days=3)
    OrderShipment.objects.create(
        order=order,
        shipment_type=shipment_type,
        shipping_date=shipping_date,  # need to ask about detail
        shipment_price=shipment_type.get_total_price(),
    )


def _create_order_status(order: Order, status_type: int, estimated_delivery_time: Optional[str], commit: bool = True) -> None:
    """
    Creates an initial status for the given order.
    """
    statues = []
    valid_statues = (
        choice.ORDER_STATUS_PAYMENT_WAITING,
        choice.ORDER_STATUS_ORDER_PLACED,
        choice.ORDER_STATUS_PRODUCT_PACKAGING,
        choice.ORDER_STATUS_READY_FOR_SHIPMENT,
        choice.ORDER_STATUS_ON_THE_WAY,
        choice.ORDER_STATUS_DROPPED_IN_DELIVERY,
        choice.ORDER_STATUS_DELIVERED,
    )

    for status in valid_statues:
        estimated_time = datetime.now() + timedelta(days=status)
        obj = OrderStatus(
            order=order,
            type=status,
            estimated_time=estimated_time,
        )
        statues.append(obj)

    if commit:
        statues = OrderStatus.objects.bulk_create(statues)
    return statues


def get_order_by_id(order_id: int) -> Order:
    """
    Fetches an order from the database based on the given order ID.
    """
    try:
        order = Order.objects.get(id=order_id)
        return order
    except Order.DoesNotExist:
        return None


def get_orders_by_user(user) -> list:
    """
    Fetches all orders associated with a given user.
    """
    return (
        Order.objects.prefetch_related("order_statuses").filter(user=user).order_by("-created_at")
    )  # Order by most recent first
