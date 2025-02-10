from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class ProductBrand(BaseModel, CreatedByMixin, UpdatedByMixin):
    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
        unique=True,
        db_index=True,
    )

    class Meta:
        verbose_name = _("Product Brand")
        verbose_name_plural = _("Product Brands")

    def __str__(self):
        return f"{self.title}"
