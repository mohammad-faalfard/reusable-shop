from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, PriorityMixin, UpdatedByMixin


class BlogCategory(BaseModel, CreatedByMixin, UpdatedByMixin, PriorityMixin):
    """
    Represents a category for blog posts.

    Attributes:
        is_active (bool): Whether the category is active or not.
        title (str): The title of the category.
        priority (int): The priority of the category (used for ordering).
        logo (ImageField): The logo associated with the category.
        parent (BlogCategory): The parent category, if any.
        created_at (datetime): When the category was created.
        updated_at (datetime): Last time the category was updated.
        created_by (User): The user who created the category.
        updated_by (User): The user who last updated the category.
    """

    title = models.CharField(max_length=100, verbose_name=_("Title"))
    logo = models.ImageField(upload_to="categories/", verbose_name=_("Logo"))
    parent = models.ForeignKey(
        "self", related_name="subcategories", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Parent")
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")
