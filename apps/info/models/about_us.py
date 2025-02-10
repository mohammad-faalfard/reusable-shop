from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class AboutUs(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Model representing the 'About Us' section of the application.

    Attributes:
        text (TextField): A brief description about the organization or service. limited to 1000 characters.
    """

    text = models.TextField(
        verbose_name=_("Description"),
        validators=[MaxLengthValidator(1000)],
        help_text=_("Maximum 1000 characters"),
    )

    def __str__(self):
        return str(_("About Us Information"))

    class Meta:
        verbose_name = _("About Us")
        verbose_name_plural = _("About Us Entries")
