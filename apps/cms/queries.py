from typing import List

from apps.products.models import Product

from .models import Banner, ProductOfferItem, Slider


def get_sliders() -> List[Slider]:
    """Returns all active sliders ordered by priority."""
    return Slider.objects.active().order_by("-priority")


def get_first_banner() -> Banner | None:
    """
    Retrieves the first active banner for holder 0.
    Returns None if no banner is found.
    """
    return Banner.objects.active().filter(holder=0).first()


def get_second_banner() -> Banner | None:
    """
    Retrieves the first active banner for holder 1.
    Returns None if no banner is found.
    """
    return Banner.objects.active().filter(holder=1).first()


def get_best_offer_product(product: Product) -> ProductOfferItem | None:
    """Returns the best offer product for a given product."""
    product.offer_items.filter().order_by("-discount").first()
