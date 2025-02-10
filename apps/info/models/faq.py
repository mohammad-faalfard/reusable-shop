from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import PriorityMixin

from .faq_group import FAQGroup


class FAQ(PriorityMixin):
    """
    Model representing a Frequently Asked Question (FAQ).

    Attributes:
        title (CharField): The title of the FAQ.
        answer (TextField): The detailed answer for the FAQ, limited to 500 characters.
        faq_group (ForeignKey): The group to which this FAQ belongs.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )
    logo = models.ImageField(
        upload_to="faq_logos/",
        verbose_name=_("Logo"),
        help_text=_("An optional logo image for the FAQ."),
        null=True,
        blank=True,
    )
    answer = models.TextField(
        verbose_name=_("Answer"),
        validators=[MaxLengthValidator(500)],
        help_text=_("Maximum 500 characters"),
    )
    faq_group = models.ForeignKey(
        FAQGroup,
        on_delete=models.CASCADE,
        related_name="faqs",
        verbose_name=_("FAQ Group"),
        help_text=_("The group to which this FAQ belongs."),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
