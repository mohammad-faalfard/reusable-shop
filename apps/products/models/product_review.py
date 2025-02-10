from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core import choice
from core.models import BaseModel, CreatedByMixin, UpdatedByMixin

from .product import Product


class ProductReview(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Model representing a review for a product submitted by a user.

    Attributes:
        is_active (bool): Status of the review, determines if it is active.
        title (str): The title of the review.
        product (ForeignKey): A reference to the `Product` that is being reviewed.
        user (ForeignKey): A reference to the `User` who submitted the review.
        text (str): The content of the review written by the user.
        rating (int): The rating given by the user, typically on a scale from 1 to 5.
        is_accepted (bool): A flag indicating whether the review has been accepted (approved) for display.
        created_at (datetime): The date and time when the ProductReview was created.
        updated_at (datetime): The date and time when the ProductReview was last updated.
        updated_by (int): ID of the user who last updated the ProductReview.
        created_by (int): ID of the user who created the ProductReview.
    """

    # title = models.CharField(
    #     max_length=100,
    #     verbose_name=_("Title"),
    # )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_reviews",
        verbose_name=_("Product"),
    )
    user = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="product_review",
        verbose_name=_("User"),
    )
    text = models.TextField(
        verbose_name=_("Text"),
        validators=[MaxLengthValidator(500)],
        help_text=_("Maximum 500 characters"),
    )

    rating = models.PositiveSmallIntegerField(
        choices=choice.RATINGS,
        default=choice.RATING_EXCELLENT,
        db_index=True,
        verbose_name=_("Rating"),
    )
    is_accepted = models.BooleanField(
        default=False,
        verbose_name=_("Is Accepted"),
    )

    class Meta:
        verbose_name = _("Product Review")
        verbose_name_plural = _("Product Reviews")
        constraints = [
            # Ensure that each user can leave only one review per product.
            # This prevents duplicate reviews and enforces data integrity.
            # models.UniqueConstraint(
            #     fields=["product", "user"],
            #     name="unique_product_review_per_user",
            # )
        ]

    def __str__(self):
        return str(self.user)

    def get_stars(self):
        """
        Returns a list of integers representing the star rating for this review.

        Example:
            - If the review rating is 4, the output will be [1, 1, 1, 1, 0].
            - If the review rating is 2, the output will be [1, 1, 0, 0, 0].
        """
        return [1] * self.rating + [0] * (5 - self.rating)
