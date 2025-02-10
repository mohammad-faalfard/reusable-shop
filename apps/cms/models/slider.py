from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin, PriorityMixin, UpdatedByMixin


class Slider(BaseModel, PriorityMixin, CreatedByMixin, UpdatedByMixin):
    """
    Model representing a slider used for showcasing content in the frontend.

    Attributes:
        is_active (bool): Determines if the slider is active and displayed.
        priority (int): The display priority of the slider.
        title (str): The title of the slider.
        media (int): Reference to the media asset for the slider.
        link (str, optional): Optional link associated with the slider.
        sub_title (str): Subtitle displayed in the slider.
        button_text (str, optional): Text displayed on the button in the slider.
        created_at (datetime): The timestamp when the slider was created.
        updated_at (datetime): The timestamp when the slider was last updated.
        updated_by (int): ID of the user who last updated the slider.
        created_by (int): ID of the user who created the slider.
    """

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
    )
    media = models.FileField(
        verbose_name=_("Media"),
        upload_to="media/uploads/",
    )
    link = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Link"),
    )
    sub_title = models.CharField(
        max_length=100,
        verbose_name=_("Subtitle"),
    )
    button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_("Button Text"),
    )

    class Meta:
        verbose_name = _("Slider")
        verbose_name_plural = _("Sliders")

    def __str__(self):
        return self.title
