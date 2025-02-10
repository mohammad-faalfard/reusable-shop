from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class PrivacyPolicy(BaseModel, CreatedByMixin, UpdatedByMixin):
    """
    Model representing the Privacy Policy of the organization.

    Attributes:
        text (TextField): The text of the privacy policy. limited to 5000 characters.
    """

    text = models.TextField(
        verbose_name=_("Privacy Policy Text"),
        validators=[MaxLengthValidator(5000)],
        help_text=_("Maximum 5000 characters"),
    )

    def __str__(self):
        return str(_("Privacy Policy Information"))

    class Meta:
        verbose_name = _("Privacy Policy")
        verbose_name_plural = _("Privacy Policies")
