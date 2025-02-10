from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from core.admin import BaseModelAdmin

from .models import Coupon, CouponConsume


class CouponConsumeAdmin(BaseModelAdmin):
    list_display = ("user", "coupon", "created_at", "is_active")
    search_fields = ("user__username", "coupon__code")
    list_filter = ("coupon", "created_at", "is_active")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("is_active", "user", "coupon")}),
        (_("Timestamps"), {"fields": ("created_at", "updated_at")}),
    )


class CouponAdmin(BaseModelAdmin):
    list_display = (
        "title",
        "code",
        "valid_from",
        "valid_until",
        "total",
        "type",
        "min_cart",
        "amount",
        "max_discount_total",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "is_active",
    )
    search_fields = ("title", "code")
    list_filter = ("type", "valid_from", "valid_until", "users", "is_active")
    readonly_fields = ("created_at", "updated_at", "created_by", "updated_by")
    filter_horizontal = ("users",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "title",
                    "code",
                    "valid_from",
                    "valid_until",
                    "total",
                    "type",
                ),
            },
        ),
        (
            _("Discount Details"),
            {
                "fields": (
                    "amount",
                    "min_cart",
                    "max_discount_total",
                ),
            },
        ),
        (
            _("User Eligibility"),
            {
                "fields": ("users",),
            },
        ),
        (
            _("Timestamps"),
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
        (
            _("Audit Info"),
            {
                "fields": ("created_by", "updated_by"),
                "classes": ("collapse",),
            },
        ),
    )


admin.site.register(Coupon, CouponAdmin)
admin.site.register(CouponConsume, CouponConsumeAdmin)
