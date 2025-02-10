from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModel


class BlogBookmark(BaseModel):
    """
    Represents a bookmark for a blog post by a user.

    Attributes:
        created_at (datetime): When the bookmark was created.
        user (User): The user who created the bookmark.
        post (Post): The post that is bookmarked.
    """

    user = models.ForeignKey(
        "account.User",
        related_name="blog_bookmarks",
        on_delete=models.PROTECT,
        verbose_name=_("User"),
    )
    post = models.ForeignKey(
        "blogs.Post",
        related_name="bookmarks",
        on_delete=models.CASCADE,
        verbose_name=_("Post"),
    )

    def __str__(self):
        return f"Bookmark by {self.user} for {self.post.title}"

    class Meta:
        verbose_name = _("Blog Bookmark")
        verbose_name_plural = _("Blog Bookmarks")
