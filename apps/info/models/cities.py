from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, UpdatedByMixin

from .states import State


class City(BaseModel, UpdatedByMixin):
    """
    Model representing a city.

    Attributes:
        title (CharField): The name of the city, limited to 100 characters.
        state (ForeignKey): Reference to the State model to which the city belongs.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
        db_index=True,
    )
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        related_name="cities",
        verbose_name=_("State"),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
