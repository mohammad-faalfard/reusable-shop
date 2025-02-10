from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from core.models import BaseModel


class ProductImage(BaseModel):
    """
    Represents an image associated with a product.

    Attributes:
        product (ForeignKey): The product this image is associated with.
        image (ResizedImageField): The uploaded image file with resizing options.
        alt_text (str): Alternative text for accessibility.
        created_at (datetime): Timestamp when the image was uploaded.
    """

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="product_images",
        verbose_name=_("Product"),
    )
    image = ResizedImageField(
        verbose_name=_("Image"),
        upload_to="products/images/",
        null=True,
        blank=True,
        force_format="WEBP",
        scale=1,
        quality=100,
    )

    alt_text = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Alt Text"),
    )

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return self.alt_text or f"Image for {self.product.title}"
