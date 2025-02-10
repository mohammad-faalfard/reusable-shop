from django.db import models
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField

from core import choice
from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class Banner(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Model representing a banner displayed in specific sections of the frontend.

    Attributes:
        is_active (bool): Determines if the banner is active and displayed.
        title (str): The title of the banner.
        image (int): Reference to the image asset for the banner.
        link (str, optional): Optional link associated with the banner.
        text (str): Text content displayed on the banner.
        button_text (str, optional): Text displayed on the button in the banner.
        holder (str): Placement of the banner in the frontend.
        created_at (datetime): The timestamp when the banner was created.
        updated_at (datetime): The timestamp when the banner was last updated.
        updated_by (int): ID of the user who last updated the banner.
        created_by (int): ID of the user who created the banner.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )
    image = ResizedImageField(
        verbose_name=_("Image"),
        upload_to="banner/images/",
        force_format="WEBP",
        scale=1,
        quality=100,
    )
    link = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_("Link"),
        help_text=_("Optional link to associate with the banner."),
    )
    text = models.TextField(
        verbose_name=_("Text"),
    )
    button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Button Text"),
    )
    holder = models.PositiveSmallIntegerField(
        choices=choice.HOLDERS,
        verbose_name=_("Holder"),
        help_text=_("Placement of the banner in the frontend."),
    )

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")
        constraints = [
            # Ensure that only one active banner exists for each holder.
            # This prevents displaying multiple banners in the same placement at the same time.
            models.UniqueConstraint(
                fields=["holder", "is_active"],
                name="unique_holder_is_active",
            )
        ]

    def __str__(self):
        return self.title
