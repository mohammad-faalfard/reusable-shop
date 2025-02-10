from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.db.models import Avg
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _

from core.models import AnalyticsBaseModel, BaseModel, CreatedByMixin, UpdatedByMixin


class Product(BaseModel, CreatedByMixin, UpdatedByMixin, AnalyticsBaseModel):
    """
    Model representing a product available in the store.

    Attributes:
        is_active (bool): Status of the product, determines if it is visible.
        title (str): The name of the product.
        category (ForeignKey): Category to which the product belongs.
        stock (int): Number of units available for this product.
        description (str): Detailed information about the product.
        price (Decimal): The price of the product.
        variants (ManyToManyField): Variants of the same product (same type but different attributes).
        created_at (datetime): The date and time when the product was created.
        updated_at (datetime): The date and time when the product was last updated.
        updated_by (int): ID of the user who last updated the product.
        created_by (int): ID of the user who created the product.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )
    category = models.ForeignKey(
        "products.ProductCategory",
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Category"),
    )
    brand = models.ForeignKey(
        "products.ProductBrand",
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name=_("Brand"),
        null=True,
        blank=False,
    )
    stock = models.PositiveIntegerField(
        verbose_name=_("Stock"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        validators=[MaxLengthValidator(3000)],
        help_text=_("Maximum 3000 characters"),
    )
    price = models.IntegerField(
        verbose_name=_("Price"),
        validators=[MinValueValidator(0), MaxValueValidator(999999999)],
    )
    tags = models.ManyToManyField(
        "ProductTag",
        blank=True,
        verbose_name=_("Tags"),
    )
    variants = models.ManyToManyField(
        "self",
        blank=True,
        verbose_name=_("Variants"),
    )

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return f"{self.title} - ({self.id})"

    def get_rating(self) -> dict:
        """
        Returns a dictionary containing the product's rating information, including
        a merged list of filled and empty stars, the  average rating, and
        the count of accepted reviews.

        The dictionary includes:
            - "stars": A list of integers where 1 represents a filled star and 0 represents
            an empty star, based on the  average rating (e.g., [1, 1, 1, 1, 0] for 4 stars).
            - "review_count": The total number of accepted reviews for the product.
            - "avg_rating": The  average rating value as an integer (1-5).

        Example output:
            {
                "stars": [1, 1, 1, 1, 0],  # 4 filled stars and 1 empty star
                "review_count": 15,         # 15 accepted reviews
                "avg_rating": 4             # Average rating  to 4
            }
        """

        # Aggregate the average rating of accepted reviews
        avg_rating = self.product_reviews.filter(is_accepted=True).aggregate(
            avg_rating=Coalesce(Avg("rating"), 0.0),
        )["avg_rating"]

        # Count the total number of accepted reviews
        review_count = self.product_reviews.filter(is_accepted=True).count()

        # Round the average rating to 2 decimal places
        avg_rating_value = round(avg_rating, 2)

        # Round the average rating to the nearest integer for stars
        avg_rating_rounded = round(avg_rating)

        # Create the merged list of stars (1s for filled, 0s for empty)
        stars = [1] * avg_rating_rounded + [0] * (5 - avg_rating_rounded)

        # Return a dictionary with the merged list of stars, average rating, review count.
        return {
            "stars": stars,
            "review_count": review_count,  # Count of accepted reviews
            "avg_rating": avg_rating_value,
        }

    @property
    def discount_info(self):
        from apps.products.queries import calculate_product_discount

        discount = calculate_product_discount(self, 1)
        return discount

    @property
    def price_with_discount(self):
        return self.discount_info[2]

    @property
    def discount_amount(self):
        return self.price - self.price_with_discount

    @property
    def discount_percent(self):
        return self.discount_info[0]

    @property
    def has_discount(self):
        return self.discount_amount > 0

    @property
    def best_offer(self):
        from apps.products.queries import get_best_offer

        best_offer = get_best_offer(self)
        return best_offer

    @property
    def best_offer_end_date_str(self):
        return self.best_offer.product_offer.active_until.strftime("%Y/%m/%d %H:%M:%S")

    @property
    def is_in_wishlist(self):
        """Before Using This Property Be Share That Method `annotate_in_wishlist` Is Applied On Queryset"""
        in_wishlist = getattr(self, "in_wishlist", False)

        return in_wishlist

    def calculate_remaining_stock(self) -> int:
        """
        Calculate the total remaining stock for the product across all offers.

        Returns:
            int: The total remaining stock for the product.
        """
        total_remaining_stock = 0

        for offer_item in self.offers.all():
            if offer_item.stock:
                total_remaining_stock += offer_item.stock - offer_item.sold_stock

        return total_remaining_stock
