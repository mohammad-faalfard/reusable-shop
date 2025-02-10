from django.contrib import admin
from unfold.admin import StackedInline

from core.admin import BaseModelAdmin

from .models import Banner, ProductOffer, ProductOfferItem, Slider


class ProductOfferItemInline(StackedInline):
    model = ProductOfferItem
    tab = True
    extra = 0
    readonly_fields = ("sold_stock",)
    autocomplete_fields = ("product_offer",)
    fieldsets = (
        (
            "Item Details",
            {
                "classes": ["tab"],
                "fields": (
                    (
                        (
                            "product_offer",
                            "product",
                        ),
                        (
                            "stock",
                            "sold_stock",
                            "discount",
                        ),
                    )
                ),
            },
        ),
    )


# Banner Admin
@admin.register(Banner)
class BannerAdmin(BaseModelAdmin):
    list_display = (
        "title",
        "is_active",
        "holder",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
    list_filter = ("is_active", "holder")
    search_fields = ("title", "text")
    ordering = ("-created_at",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "title",
                    "image",
                    "link",
                    "text",
                    "button_text",
                    "holder",
                )
            },
        ),
    )


# Product Offer Admin
@admin.register(ProductOffer)
class ProductOfferAdmin(BaseModelAdmin):
    list_display = (
        "title",
        "active_from",
        "active_until",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )
    list_filter = ("active_from", "active_until")
    search_fields = ("title",)
    ordering = ("-active_from",)
    inlines = [
        ProductOfferItemInline,
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "title",
                    "active_from",
                    "active_until",
                )
            },
        ),
    )


# Product Offer Item Admin
@admin.register(ProductOfferItem)
class ProductOfferItemAdmin(BaseModelAdmin):
    list_display = (
        "product",
        "product_offer",
        "stock",
        "sold_stock",
        "discount",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "is_active",
    )
    list_filter = ("is_active",)
    search_fields = ("product__title",)
    readonly_fields = ("sold_stock",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "product",
                    "product_offer",
                    "stock",
                    "sold_stock",
                    "discount",
                )
            },
        ),
    )


# Slider Admin
@admin.register(Slider)
class SliderAdmin(BaseModelAdmin):
    list_display = (
        "title",
        "priority",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "is_active",
    )
    list_filter = ("is_active", "priority")
    search_fields = ("title", "sub_title")
    ordering = ("-priority",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "priority",
                    "title",
                    "media",
                    "link",
                    "sub_title",
                    "button_text",
                )
            },
        ),
    )
