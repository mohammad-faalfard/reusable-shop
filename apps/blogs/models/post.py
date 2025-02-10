from django.core.validators import MaxLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_SAVE, LifecycleModel, hook

from core.models import BaseModel, CreatedByMixin, UpdatedByMixin


class Post(BaseModel, CreatedByMixin, UpdatedByMixin, LifecycleModel):
    """
    Represents a blog post.

    Attributes:
        title (str): Title of the post.
        category (Category): The category to which the post belongs.
        text (str): The content of the post.
        tags (ManyToManyField): Tags associated with the post.
        read_time (int): Estimated time to read the post in minutes (stored in database).
        image (ImageField): Optional image for the post.
        created_at (datetime): When the post was created.
        updated_at (datetime): Last time the post was updated.
        created_by (User): The user who created the post.
        updated_by (User): The user who last updated the post.
    """

    title = models.CharField(max_length=100, verbose_name=_("Title"))
    category = models.ForeignKey(
        "BlogCategory",
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name=_("Category"),
    )
    text = models.TextField(validators=[MaxLengthValidator(5000)], verbose_name=_("Content"))
    tags = models.ManyToManyField("Tag", related_name="posts", verbose_name=_("Tags"))
    read_time = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_("Read Time (minutes)"),
        help_text=_("Estimated time to read the post in minutes. Calculated based on word count."),
    )
    image = models.ImageField(upload_to="posts/", verbose_name=_("Image"))

    def __str__(self):
        return self.title

    def calculate_read_time(self):
        """
        Calculate the reading time based on the content of the post.
        Assumes an average reading speed of 200 words per minute.
        """
        word_count = len(self.text.split())  # Count words in the text
        return max(1, word_count // 200)  # Return at least 1 minute

    @hook(AFTER_SAVE)
    def update_read_time(self):
        """
        This hook updates the `read_time` field after the model is saved.
        It ensures that the reading time is recalculated based on the updated text.
        """
        self.read_time = self.calculate_read_time()

    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")
