from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class Tag(BaseModel):
    """
    Represents a tag for categorizing blog posts.

    Attributes:
        name (str): The name of the tag.
        created_at (datetime): When the tag was created.
    """

    name = models.CharField(max_length=100, verbose_name=_("Tag Name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
