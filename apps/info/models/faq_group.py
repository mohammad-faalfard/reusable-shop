from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, PriorityMixin, UpdatedByMixin


class FAQGroup(BaseModel, UpdatedByMixin, PriorityMixin):
    """
    Model representing a group of Frequently Asked Questions (FAQs).

    Attributes:
        title (CharField): The title of the FAQ group.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )

    def __str__(self):
        return f"{self.id} - {self.title}"

    class Meta:
        verbose_name = _("FAQ Group")
        verbose_name_plural = _("FAQ Groups")
