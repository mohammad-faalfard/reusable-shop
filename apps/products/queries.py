# queries.py
from collections import defaultdict
from typing import List

from django.db.models import BooleanField, Exists, F, OuterRef, Q, QuerySet, Value
from django.utils import timezone
from django.utils.timezone import now

from apps.account.models import User
from core import choice

from .models import Product, ProductCategory, ProductReview, ProductWishlist


def get_all_products(user: User = None) -> list[Product]:
    """
    Fetch all active products for display. If a user is provided, annotate
    each product with additional user-specific data, such as whether the
    product is in the user's wishlist.
    """
    qs = (
        Product.objects.filter(is_active=True)
        .select_related("category")
        .prefetch_related(
            "offers",
            "discounts",
            "product_images",
        )
    )

    # Annotate in_wishlist on DB side to improve performance
    qs = annotate_in_wishlist(qs, user)
    return qs


def annotate_in_wishlist(product_qs: QuerySet, user: User = None) -> QuerySet:
    """
    Annotate the product queryset with 'in_wishlist' to check if each product
    is in the given user's wishlist. Optimized for performance by handling it
    at the database level.

    Args:
        product_qs (QuerySet): The queryset of products to annotate.
        user (User, optional): The current user. Defaults to None.

    Returns:
        QuerySet: The product queryset annotated with 'in_wishlist' as a boolean.
    """

    wishlist_subquery = ProductWishlist.objects.filter(user=user, product=OuterRef("pk"))
    if user and user.is_authenticated:
        product_qs = product_qs.annotate(in_wishlist=Exists(wishlist_subquery))
    else:
        product_qs = product_qs.annotate(in_wishlist=Value(False, BooleanField()))

    return product_qs


def get_best_offer(product: Product):
    offer = (
        product.offers.filter(
            # Active Check
            is_active=True,
            product_offer__is_active=True,
        )
        .filter(
            # Stock Checks
            Q(stock__isnull=True)  # Without Stock Limit
            | (  # Stock Limit
                Q(stock__isnull=False)
                & Q(
                    stock__gt=F("sold_stock"),
                )
            )
        )
        .filter(
            # Active And End Times
            Q(product_offer__active_from__lte=now())
            & Q(
                product_offer__active_until__gte=now(),
            )
        )
        .order_by("-discount")  # Maximum Discount
        .first()
    )
    return offer


def get_best_discount(product: Product):
    # Product Discount
    discount = (
        product.discounts.filter(
            # Active And End Times
            (Q(active_from__isnull=True) | Q(active_from__lte=now()))
            & (Q(active_until__isnull=True) | Q(active_until__gte=now()))
        )
        .filter(is_active=True)
        .first()
    )
    return discount


def calculate_product_discount(product: Product, quantity: int = 1) -> list[float, float, float]:
    """
    Calculate the optimal discount for a product based on its offers and general discounts.

    This function determines the maximum discount that can be applied to a product by evaluating
    its current active offer and general discount. It calculates the discount amount and the
    final unit price based on the requested quantity and available stock for the offer.

    Args:
        product (Product): The product for which the discount is being calculated.
        quantity (int): Number of units of the product (default is 1).

    Returns:
        list[float, float, float]: A list containing:
            - Maximum discount percentage applied (float).
            - Total With discount amount for the given quantity (float).
            - Final price per unit after applying the best discount (float).

    Methodology:
        - Fetch the best available offer and general discount for the product.
        - Compare their discount percentages to identify the better deal.
        - Divide the requested quantity between offer and general discount:
            - Offer quantities are capped by the remaining offer stock.
            - The rest are calculated using the general discount.
        - Calculate the total discount and the minimum price per unit.
        - Ensure no discount exceeds 100%.

    Notes:
        - If the product has no valid price, offer, or discount, no discount is applied.
        - Handles zero or negative input for quantity gracefully by returning zeros.
    """

    if product.price <= 0 or quantity <= 0:
        return 0.0, 0.0, 0.0

    # Get the best available offer and discount for the product
    offer = get_best_offer(product)
    discount = get_best_discount(product)

    product_price = product.price
    offer_discount_percent = offer.discount if offer else 0.0
    discount_percent = 0.0

    if discount:
        if discount.type == choice.DISCOUNT_TYPE_AMOUNT:
            discount_percent = (discount.amount / product_price) * 100
        elif discount.type == choice.DISCOUNT_TYPE_PERCENT:
            discount_percent = discount.amount

    # Determine which discount is better
    is_offer_better = offer_discount_percent > discount_percent
    remaining_offer_quantity = max(0, (offer.stock - offer.sold_stock)) if offer else 0

    # Calculate quantities for offer and discount
    quantity_on_offer = min(remaining_offer_quantity, quantity) if is_offer_better else 0
    quantity_on_discount = quantity - quantity_on_offer

    # Calculate price per unit for both offer and discount
    price_per_unit_offer = product_price * (1 - offer_discount_percent / 100)
    price_per_unit_discount = product_price * (1 - discount_percent / 100)

    # Calculate total discount amounts
    total_offer_price = quantity_on_offer * price_per_unit_offer
    total_discount_price = quantity_on_discount * price_per_unit_discount
    total_with_discount = total_offer_price + total_discount_price

    # Final price per unit (lowest possible price)
    final_price_per_unit = min(price_per_unit_offer, price_per_unit_discount)

    # Maximum discount percentage
    maximum_discount = max(offer_discount_percent, discount_percent)
    maximum_discount = min(maximum_discount, 100)  # Ensure the discount does not exceed 100%

    return maximum_discount, total_with_discount, final_price_per_unit


def get_product_categories() -> list[ProductCategory]:
    """
    Fetches all active product categories.
    """
    return ProductCategory.objects.active().filter(parent__isnull=True).distinct("id")


def get_subcategories_for_category(parent_category: ProductCategory) -> list[ProductCategory]:
    """
    Fetches subcategories for a given parent category.
    """
    return parent_category.get_descendants().order_by("-priority")


def get_product_category(id: int) -> ProductCategory | None:
    return ProductCategory.objects.filter(is_active=True, pk=id).first()


def get_products_by_category(category: ProductCategory, user: User = None) -> list[Product]:
    """Fetch products for a specific category and its subcategories without duplicates."""
    sub_cats = category.get_descendants(True)
    qs = get_all_products(user).filter(category__in=sub_cats).distinct().order_by("-created_at")
    return qs


def get_products_by_subcategory(category_id: int) -> list[Product]:
    """Fetch products for a specific subcategory."""
    return Product.objects.active().filter(category_id=category_id).order_by("-created_at")


def get_product(product_id: int, user: User = None) -> Product | None:
    """
    Fetch a single product by its ID. If a user is provided, annotate the product with user-specific
    data, such as whether the product is in the user's wishlist.
    """
    product = (
        Product.objects.active()
        .prefetch_related(
            "product_images",
            "product_properties",
            "variants",
            "offers",
            "discounts",
        )
        .filter(
            id=product_id,
        )
    )
    qs = annotate_in_wishlist(product, user)

    return qs.first()


def get_product_details_by_id(product_id: int, user: User = None):
    """
    Fetch a single product by its ID, including related images and properties,
    grouped by title for easy rendering of radio buttons.
    """

    product = get_product(product_id, user)
    if not product:
        return None

    # Group properties by title
    grouped_properties = defaultdict(list)
    for property in product.product_properties.all():
        grouped_properties[property.title].append(property)
    # Fetch related variants
    product_discount = calculate_product_discount(product, 1)
    return {
        "product": product,
        "product_images": product.product_images.all(),
        "grouped_product_properties": dict(grouped_properties),
        "discount_percent": product_discount[0],
        "discount_amount": product_discount[1],
        "final_price": product_discount[2] or product.price,
    }


def get_related_products(product_id: int) -> list[Product]:
    """
    Fetch all products related to the given product by its ID using the variants field.
    """
    try:
        product = Product.objects.active().get(id=product_id)
        return product.variants.all()
    except Product.DoesNotExist:
        # Return an empty list if the product does not exist
        return []


def get_product_reviews(product: Product) -> list[ProductReview]:
    """
    Fetch active reviews for a specific product.
    """
    return product.product_reviews.filter(
        product=product,
        is_accepted=True,
    ).order_by("-created_at")


def has_user_reviewed_product(product_id: int, user_id: int):
    """
    Check if the user has already reviewed a specific product.
    """
    try:
        product = Product.objects.get(id=product_id)
        return product.product_reviews.filter(user__id=user_id).exists()
    except Product.DoesNotExist:
        return False


def get_sorted_products(category_id: int = None, selected_sort_option: str = "1") -> List[Product]:
    """
    Retrieves and sorts products based on the selected category and sorting criteria.

    Parameters:
        category_id (int, optional): The ID of the product category to filter by. Defaults to None.
        selected_sort_option (str, optional): The sorting criteria:
            - '1' for sorting by newest (default).
            - '2' for sorting by most viewed.
            - '3' for sorting by ratings (not implemented in the current logic).

    Returns:
        List[Product]: A list of products filtered and sorted based on the specified criteria.

    Example:
        get_sorted_products(category_id=5, sort_by="2")
        # Returns products in category 5, sorted by most viewed.
    """

    products = Product.objects.all()

    # Filter by category if category_id is provided
    if category_id:
        products = products.filter(category_id=category_id)

    # Sorting logic based on the 'selected_sort_option' parameter
    if selected_sort_option == choice.SORT_NEWEST:
        products = products.order_by("-created_at")
    elif selected_sort_option == choice.SORT_MOST_VIEWED:
        products = products.order_by("-view_count")

    return products


def get_user_wishlist(user: User) -> List[Product]:
    """Get all active wishlist items for a specific user."""
    products = get_all_products(user).filter(product_wish_list__user=user, product_wish_list__is_active=True)
    return products


def is_product_in_wishlist(user: User, product: Product):
    """Check if a product is in the user's wishlist."""
    return product.product_wish_list.filter(user=user).exists()


def add_or_remove_product_from_wishlist(user_id: int, product_id: int) -> int:
    """
    Add a product to the user's wishlist if it doesn't exist,
    or remove it if it already exists.

    Args:
        user_id (int): The ID of the user.
        product_id (int): The ID of the product to toggle in the wishlist.

    Returns:
        int: Returns 1 if the product was added, 0 if the product was removed.
    """
    # Check if the product already exists in the wishlist
    wishlist_item = ProductWishlist.objects.filter(user_id=user_id, product_id=product_id).first()

    if wishlist_item:
        # If it exists, remove the product from the wishlist
        wishlist_item.delete()
        return 0  # Product removed
    else:
        # If it doesn't exist, add the product to the wishlist
        ProductWishlist.objects.create(user_id=user_id, product_id=product_id)
        return 1  # Product added


def clear_user_wishlist(user_id: int) -> None:
    """Delete all wishlist items for a user."""
    ProductWishlist.objects.filter(user_id=user_id).delete()


def get_wishlist_count(user_id: int) -> int:
    """Get the count of active wishlist items for a user."""
    return ProductWishlist.objects.filter(user_id=user_id, is_active=True).count()


def create_product_review(product: Product, user: User, star: int, comment: str) -> None:
    """Create a new product review."""
    rating_map = {
        1: choice.RATING_POOR,
        2: choice.RATING_AVERAGE,
        3: choice.RATING_GOOD,
        4: choice.RATING_VERY_GOOD,
        5: choice.RATING_EXCELLENT,
    }
    obj = ProductReview.objects.create(
        product=product,
        user=user,
        text=comment,
        rating=rating_map.get(star, choice.RATING_EXCELLENT),
        is_accepted=True,
    )
    return obj


def search_products(query: str, user: User = None) -> list[Product]:
    """Search products based on a query string."""
    qs = (
        get_all_products(user)
        .filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(category__title__icontains=query),
        )
        .distinct()
        .order_by("-created_at")
    )
    return qs


def get_products_with_offers(products: list[Product]) -> dict:
    """
    Fetch all active products that have offers, grouped by product offer,
    excluding expired offers and offers that have not yet started.
    Optimized for efficient database queries.
    """
    # Get the current time
    now = timezone.now()

    # Retrieve products and offers in one optimized query
    products_with_offers = products.filter(offers__isnull=False).prefetch_related("offers__product_offer").distinct()

    # Create a defaultdict to group products by their associated product offer
    products_by_offer = defaultdict(list)

    # Iterate through the products and group them by their associated product offer
    for product in products_with_offers:
        active_offer_items = product.offers.filter(
            product_offer__is_active=True,
            product_offer__active_from__lte=now,
            product_offer__active_until__gte=now,
            stock__gt=F("sold_stock"),  # Ensure stock is greater than sold stock
        )

        for offer_item in active_offer_items:
            products_by_offer[offer_item.product_offer].append(product)

    # Reverse the order of products (if needed, reverse after processing)
    products_by_offer = {key: value[::-1] for key, value in products_by_offer.items()}

    return products_by_offer
