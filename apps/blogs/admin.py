from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin import BaseModelAdmin

from .models import BlogBookmark, BlogCategory, Post, PostComment, Tag


# Tag Admin
@admin.register(Tag)
class TagAdmin(BaseModelAdmin):
    """Admin interface for the Tag model."""

    list_display = ("id", "name", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    fields = ("name", "created_at")
    readonly_fields = ("created_at",)


# Post Admin
@admin.register(Post)
class PostAdmin(BaseModelAdmin):
    """Admin interface for the Post model."""

    list_display = ("id", "is_active", "title", "category", "read_time", "created_at", "updated_at")
    list_filter = ("category", "created_at", "updated_at")
    search_fields = ("title", "text")
    ordering = ("-created_at",)
    filter_horizontal = ("tags",)
    fieldsets = (
        (
            None,
            {"fields": ("is_active", "title", "text", "category", "tags", "image", "read_time")},
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at", "updated_at")


# PostComment Admin
@admin.register(PostComment)
class PostCommentAdmin(BaseModelAdmin):
    """Admin interface for the PostComment model."""

    list_display = ("id", "is_active", "sender", "post", "is_accepted", "created_at", "edited_at")
    list_filter = ("is_accepted", "created_at", "edited_at")
    search_fields = ("text", "sender__username")
    ordering = ("-created_at",)
    fieldsets = (
        (
            None,
            {"fields": ("post", "sender", "text", "is_accepted", "reply")},
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "edited_at"),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("created_at", "edited_at")


# BlogCategory Admin
@admin.register(BlogCategory)
class BlogCategoryAdmin(BaseModelAdmin):
    """Admin interface for the BlogCategory model."""

    list_display = ("id", "is_active", "title", "parent", "priority", "created_at")
    list_filter = ("parent", "created_at")
    search_fields = ("title",)
    ordering = ("priority", "title")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "priority",
                    "title",
                    "logo",
                    "parent",
                )
            },
        ),
        (_("Timestamps"), {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
    readonly_fields = ("created_at", "updated_at")


# BlogBookmark Admin
@admin.register(BlogBookmark)
class BlogBookmarkAdmin(BaseModelAdmin):
    """Admin interface for the BlogBookmark model."""

    list_display = ("id", "user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "post__title")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
