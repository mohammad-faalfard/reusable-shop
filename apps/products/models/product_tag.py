from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class ProductTag(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Model representing a tag assigned to products, allowing products to be
    grouped and filtered based on certain attributes or themes.

    Attributes:
        is_active (bool): Status of the tag, determines if it is visible.
        title (str): The name of the tag.
        created_at (datetime): The date and time when the tag was created.
        updated_at (datetime): The date and time when the tag was last updated.
        updated_by (int): ID of the user who last updated the tag.
        created_by (int): ID of the user who created the tag.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )

    class Meta:
        verbose_name = _("Product Tag")
        verbose_name_plural = _("Product Tags")

    def __str__(self):
        return self.title
