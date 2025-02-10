from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, PriorityMixin


class InquiryCategory(BaseModel, PriorityMixin):
    """
    Represents categories for user inquiries.
    """

    title = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("title"),
        help_text=_("The title of the inquiry category (e.g., Buying Support)."),
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Inquiry Category")
        verbose_name_plural = _("Inquiry Categories")
        ordering = ["-priority"]


class ContactUs(BaseModel, CreatedByMixin):
    """
    Represents a user inquiry submitted via the Contact Us form.

    Attributes:
        name (CharField): The name of the user submitting the inquiry.
        email (EmailField): The email address of the user.
        subject (CharField): The subject of the inquiry.
        message (TextField): The detailed message from the user.
        relevant_url (URLField): An optional URL relevant to the user's inquiry.
        category (ForeignKey): Links the inquiry to a specific category.
    """

    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("The name of the person submitting the inquiry."),
    )
    email = models.EmailField(
        verbose_name=_("Email Address"),
        help_text=_("The email address of the person submitting the inquiry."),
    )
    subject = models.CharField(
        max_length=150,
        verbose_name=_("Subject"),
        help_text=_("The subject of the inquiry."),
    )
    message = models.TextField(
        verbose_name=_("Message"),
        help_text=_("The detailed message from the person submitting the inquiry."),
        validators=[MaxLengthValidator(500)],  # Limit message to 500 characters
    )

    relevant_url = models.URLField(
        verbose_name=_("Relevant URL"),
        help_text=_("An optional URL relevant to your inquiry (e.g., a related webpage)."),
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        InquiryCategory,
        on_delete=models.PROTECT,
        verbose_name=_("Category"),
        help_text=_("Select the category of the inquiry."),
    )

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.category})"

    class Meta:
        verbose_name = _("Contact Us Inquiry")
        verbose_name_plural = _("Contact Us Inquiries")
        ordering = ["-created_at"]
