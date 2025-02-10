from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel, CreatedByMixin


class PostComment(BaseModel, CreatedByMixin):
    """
    Represents a comment on a blog post.

    Attributes:
        post (Post): The blog post the comment is associated with.
        is_active (bool): Whether the comment is active or not.
        created_at (datetime): When the comment was created.
        created_by (User): The user who created the comment.
        edited_at (datetime): Last time the comment was edited.
        is_accepted (bool): Whether the comment has been accepted.
        text (str): The content of the comment.
        reply (PostComment): The comment that this comment is replying to, if any.
        sender (User): The user who sent the comment.
    """

    post = models.ForeignKey(
        "blogs.Post",
        related_name="comments",
        on_delete=models.CASCADE,
        verbose_name=_("Post"),
    )
    edited_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Edited At"),
    )
    is_accepted = models.BooleanField(
        default=False,
        verbose_name=_("Accepted"),
    )
    text = models.CharField(
        max_length=200,
        verbose_name=_("Comment Text"),
    )
    reply = models.ForeignKey(
        "self",
        related_name="replies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Reply to"),
    )
    sender = models.ForeignKey(
        "account.User",
        related_name="sent_comments",
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("Sender"),
    )

    def __str__(self):
        return self.text

    def clean(self):
        """Ensure a user cannot reply to their own comment."""
        if self.reply and self.sender == self.reply.sender:
            raise ValidationError(_("You cannot reply to your own comment."))

    class Meta:
        verbose_name = _("Post Comment")
        verbose_name_plural = _("Post Comments")
