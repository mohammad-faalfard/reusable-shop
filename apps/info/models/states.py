from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, PriorityMixin, UpdatedByMixin


class State(BaseModel, UpdatedByMixin, PriorityMixin):
    """
    Model representing a state or province.

    Attributes:
        title (CharField): The name of the state, limited to 100 characters, and must be unique.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
        unique=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")
