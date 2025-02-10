from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin import BaseModelAdmin, format_html

from .models import ShipmentType


@admin.register(ShipmentType)
class ShipmentTypeAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "title",
        "service_type",
        "price",
        "vat",
        "logo_preview",  # logo_preview method to show the image
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "is_active",
    )
    list_filter = ("is_active", "service_type", "created_at")
    search_fields = ("title", "description")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "title",
                    "service_type",
                    "description",
                    "logo",
                    "price",
                    "vat",
                ),
            },
        ),
    )

    def logo_preview(self, obj):
        """
        Method to display a thumbnail of the logo in the admin list view.
        """
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        return "No Logo"

    logo_preview.short_description = _("Logo")
