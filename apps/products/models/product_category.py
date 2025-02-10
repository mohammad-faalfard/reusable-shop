from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from core.models import BaseModel, CreatedByMixin, PriorityMixin, UpdatedByMixin


class ProductCategory(BaseModel, CreatedByMixin, PriorityMixin, UpdatedByMixin, MPTTModel):
    """
    Model representing a category of products. Categories help organize products
    into a hierarchy, making it easier for users to browse and find items.

    Attributes:
        is_active (bool): Status of the category, determines if it is visible.
        priority (int): Determines the order in which categories are displayed.
        title (str): The name of the category.
        parent (ProductCategory): Self-referencing foreign key to allow hierarchical categories.
        logo (ImageField): Image representing the category.
        description (str): Additional information about the category.
        created_at (datetime): The date and time when the category was created.
        updated_at (datetime): The date and time when the category was last updated.
        updated_by (int): ID of the user who last updated the category.
        created_by (int): ID of the user who created the category.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )
    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_("Parent"),
        related_name="children",
    )
    logo = models.ImageField(
        upload_to="category_logos/",
        verbose_name=_("Logo"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
        validators=[MaxLengthValidator(3000)],
        help_text=_("Maximum 3000 characters"),
    )

    class Meta:
        verbose_name = _("Product Category")
        verbose_name_plural = _("Product Categories")

    def __str__(self):
        return self.title
