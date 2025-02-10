# apps/account/models/address.py

from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel
from core.models.mixins import UpdatedByMixin


class Address(BaseModel, UpdatedByMixin):
    """
    Represents a user's address.

    Attributes:
        user (ForeignKey): The user associated with this address.
        title (CharField): A title or nickname for the address.
        postal_code (CharField): The postal code for the address (optional).
        street (CharField): The street address.

    Methods:
        __str__(): Returns a string representation of the address, including the title and username of the associated user.
    """

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name=_("User"),
    )
    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Postal Code"),
    )
    city = models.ForeignKey(
        "info.City",
        on_delete=models.PROTECT,
        related_name="addresses",
        verbose_name=_("City"),
    )
    street = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Street"),
    )

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
