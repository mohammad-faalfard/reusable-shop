from django.contrib import admin
from unfold.admin import StackedInline, TabularInline

from core.admin import BaseModelAdmin

from .models import Order, OrderItem, OrderShipment, OrderStatus


class OrderStatusInline(TabularInline):
    model = OrderStatus
    tab = True
    extra = 0
    exclude = ("updated_by", "created_by")


class OrderItemInline(StackedInline):
    model = OrderItem
    tab = True
    extra = 0
    readonly_fields = ("product_price", "product_discount")
    autocomplete_fields = ("product",)
    fieldsets = (
        (
            "Item Details",
            {
                "classes": ["tab"],
                "fields": (
                    (
                        (
                            "product",
                            "product_price",
                            "product_discount",
                        ),
                        (
                            "quantity",
                            "price",
                        ),
                    )
                ),
            },
        ),
    )


class OrderShipmentInline(TabularInline):
    model = OrderShipment
    tab = True
    extra = 0
    fieldsets = (
        (
            None,
            {
                "classes": ["tab"],
                "fields": (
                    "shipment_type",
                    "shipping_date",
                    "shipment_price",
                ),
            },
        ),
    )

    def has_add_permission(self, request, *args):
        return False

    def has_delete_permission(self, request, obj=..., *args):
        return False


# Customizing the admin view for Order
@admin.register(Order)
class OrderAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "user",
        "address",
        "coupon",
        "product_total_price",
        "coupon_total_discount",
        "product_total_discount",
        "note",
        "total_price",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "is_active",
        "current_status",
    )
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    inlines = [OrderItemInline, OrderShipmentInline, OrderStatusInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "user",
                    "address",
                    "coupon",
                    "note",
                    "product_total_price",
                    "coupon_total_discount",
                    "product_total_discount",
                    "shipment_price",
                    "total_price",
                    "current_status",
                )
            },
        ),
    )


# Customizing the admin view for OrderItem
@admin.register(OrderItem)
class OrderItemAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "user",
        "order",
        "product",
        "product_title",
        "product_price",
        "product_discount",
        "quantity",
        "price",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "is_active",
    )
    search_fields = ("order__id", "product__title")
    ordering = ("-created_at",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "user",
                    "order",
                    "product",
                    "product_title",
                    "product_price",
                    "product_discount",
                    "quantity",
                    "price",
                )
            },
        ),
    )


# Customizing the admin view for OrderShipment
@admin.register(OrderShipment)
class OrderShipmentAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "order",
        "shipment_type",
        "shipping_date",
        "shipment_price",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "is_active",
    )
    search_fields = ("order__id",)
    list_filter = ("shipment_type", "shipping_date")
    ordering = ("-created_at",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "order",
                    "shipment_type",
                    "shipping_date",
                    "shipment_price",
                )
            },
        ),
    )


# Customizing the admin view for OrderStatus
@admin.register(OrderStatus)
class OrderStatusAdmin(BaseModelAdmin):
    list_display = (
        "id",
        "order",
        "type",
        "timestamp",
        "estimated_time",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
        "is_active",
    )
    search_fields = ("order__id",)
    list_filter = ("type", "timestamp")
    ordering = ("-created_at",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "order",
                    "type",
                    "estimated_time",
                )
            },
        ),
    )
