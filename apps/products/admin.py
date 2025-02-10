from django.contrib import admin
from unfold.admin import StackedInline

from apps.products.models.product_brand import ProductBrand
from core.admin import BaseModelAdmin

from .forms import ProductAdminForm
from .models import (
    Product,
    ProductCategory,
    ProductDiscount,
    ProductImage,
    ProductProperty,
    ProductReview,
    ProductTag,
    ProductWishlist,
)


class ProductImageInline(StackedInline):
    model = ProductImage
    extra = 0  # Allow no extra empty form
    fields = ["image", "alt_text"]
    max_num = 5  # Limit the number of images per product
    tab = True


class ProductPropertyInline(StackedInline):
    model = ProductProperty
    extra = 0  # Allow no extra empty form
    fields = ["title", "value"]
    tab = True


class ProductTagInline(StackedInline):
    model = ProductTag
    extra = 0  # Allow no extra empty form
    fields = ["title", "is_active"]
    tab = True


class ProductDiscountInline(StackedInline):
    model = ProductDiscount
    extra = 0  # Allow no extra empty form
    fields = [
        "title",
        "type",
        "amount",
        "active_from",
        "active_until",
        "is_active",
    ]
    max_num = 5  # Limit the number of images per product
    tab = True


# Admin configuration for Product model
class ProductAdmin(BaseModelAdmin):
    form = ProductAdminForm
    inlines = [ProductImageInline, ProductDiscountInline, ProductPropertyInline]
    # Fields to display in the list view of the admin panel
    list_display = (
        "id",
        "title",
        "price",
        "stock",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "views_count",
        "is_active",
    )
    # Fields to allow searching in the admin panel
    search_fields = ("title", "description")
    # Filters to apply in the admin panel
    list_filter = ("is_active", "category")
    # Fieldset configuration for the form layout
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "title",
                    "description",
                    "category",
                    "brand",
                    "price",
                    "stock",
                    "variants",
                    "tags",
                )
            },
        ),
    )
    filter_horizontal = ("variants", "tags")
    # Default ordering of the products based on creation date (descending)
    ordering = ("-created_at",)


# Admin configuration for ProductCategory model
class ProductCategoryAdmin(BaseModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = (
        "id",
        "title",
        "parent",
        "priority",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "is_active",
    )
    # Fields to allow searching in the admin panel
    search_fields = ("title", "description")
    # Filters to apply in the admin panel
    list_filter = ("is_active", "parent")
    # Default ordering based on priority (descending)
    ordering = ("-priority",)
    # Fieldset configuration for the form layout
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "priority",
                    "title",
                    "description",
                    "logo",
                    "parent",
                )
            },
        ),
    )


# Admin configuration for ProductDiscount model
class ProductDiscountAdmin(BaseModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = (
        "id",
        "title",
        "type",
        "amount",
        "active_from",
        "active_until",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "is_active",
    )
    # Fields to allow searching in the admin panel
    search_fields = ("title", "type")
    # Filters to apply in the admin panel
    list_filter = ("is_active", "type", "active_from", "active_until")
    # Default ordering based on creation date (descending)
    ordering = ("-created_at",)
    # Fieldset configuration for the form layout
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "product",
                    "is_active",
                    "title",
                    "type",
                    "amount",
                    "active_from",
                    "active_until",
                )
            },
        ),
    )


# Admin configuration for ProductProperty model
class ProductPropertyAdmin(BaseModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = (
        "id",
        "title",
        "value",
        "product",
        "priority",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "is_active",
    )
    # Fields to allow searching in the admin panel
    search_fields = ("title", "value", "product__title")
    # Filters to apply in the admin panel
    list_filter = ("is_active", "product")
    # Default ordering based on priority (ascending), then creation date (descending)
    ordering = ("priority", "-created_at")
    # Fieldset configuration for the form layout
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "priority",
                    "title",
                    "value",
                    "product",
                )
            },
        ),
    )


# Admin configuration for ProductReview model
class ProductReviewAdmin(BaseModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = (
        "id",
        # "title",
        "product",
        "user",
        "rating",
        "is_accepted",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "is_active",
    )
    # Fields to allow searching in the admin panel
    search_fields = ("text", "user__username")
    # Filters to apply in the admin panel
    list_filter = ("is_accepted", "rating", "product")
    # Default ordering based on creation date (descending)
    ordering = ("-created_at",)
    # Fieldset configuration for the form layout
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "product",
                    "user",
                    "rating",
                    "text",
                    "is_accepted",
                )
            },
        ),
    )


# Admin configuration for ProductTag model
class ProductTagAdmin(BaseModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = (
        "id",
        "title",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "is_active",
    )
    # Fields to allow searching in the admin panel
    search_fields = ("title",)
    # Filters to apply in the admin panel
    list_filter = ("is_active",)
    # Default ordering based on creation date (descending)
    ordering = ("-created_at",)
    # Fieldset configuration for the form layout
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "title",
                )
            },
        ),
    )


# Admin configuration for ProductTag model
class ProductBrandAdmin(BaseModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = (
        "id",
        "title",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "is_active",
    )
    # Fields to allow searching in the admin panel
    search_fields = ("title",)
    # Filters to apply in the admin panel
    list_filter = ("is_active",)
    # Default ordering based on creation date (descending)
    ordering = ("-created_at",)
    # Fieldset configuration for the form layout
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "title",
                )
            },
        ),
    )


# Admin configuration for ProductImage model
class ProductImageAdmin(BaseModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = (
        "id",
        "product",
        "image",
        "alt_text",
        "is_active",
    )
    # Filters to apply in the admin panel
    list_filter = ("is_active",)
    # Default ordering based on creation date (descending)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "product",
                    "image",
                    "alt_text",
                )
            },
        ),
    )


# Admin configuration for ProductWishlist model
class ProductWishlistAdmin(BaseModelAdmin):
    # Fields to display in the list view of the admin panel
    list_display = (
        "id",
        "user",
        "product",
        "created_at",
        "updated_at",
        "is_active",
    )
    # Fields to allow searching in the admin panel
    search_fields = ("user__username", "product__title")
    # Filters to apply in the admin panel
    list_filter = ("is_active", "product", "user")
    # Fieldset configuration for the form layout
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_active",
                    "user",
                    "product",
                )
            },
        ),
    )


# Register models with the custom admin configurations
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ProductDiscount, ProductDiscountAdmin)
admin.site.register(ProductProperty, ProductPropertyAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(ProductTag, ProductTagAdmin)
admin.site.register(ProductWishlist, ProductWishlistAdmin)
admin.site.register(ProductBrand, ProductBrandAdmin)
admin.site.register(ProductImage, ProductImageAdmin)
