from django.db.models import Avg, Count, Q
from django.utils.translation import gettext_lazy as _
from django_filters import ChoiceFilter, FilterSet, ModelMultipleChoiceFilter, MultipleChoiceFilter, NumberFilter

from apps.products.models import ProductBrand, ProductCategory
from apps.products.models.product import Product
from core import choice

SORT_CHOICES = [
    ("newest", _("Newest")),
    ("popular", _("Popular")),
    ("rating", _("Rating")),
]


class ProductListFilter(FilterSet):
    brand = ModelMultipleChoiceFilter(
        field_name="brand",
        lookup_expr="exact",
        null_label=_("Other"),
        queryset=ProductBrand.objects.filter(is_active=True),
    )
    category = ModelMultipleChoiceFilter(
        field_name="category",
        lookup_expr="exact",
        null_label=_("Other"),
        queryset=ProductCategory.objects.filter(is_active=True),
    )
    sort = ChoiceFilter(
        choices=SORT_CHOICES,
        method="filter_sorting",
        label=_("Sort By"),
    )
    rating = MultipleChoiceFilter(
        choices=choice.RATINGS,
        method="filter_by_ratings",
        label=_("Ratings"),
    )
    min_price = NumberFilter(
        field_name="price",
        lookup_expr="gte",
    )
    max_price = NumberFilter(
        field_name="price",
        lookup_expr="lte",
    )

    class Meta:
        model = Product
        fields = ["title", "brand", "category", "min_price", "max_price"]

    def filter_by_ratings(self, queryset, name, values):
        """
        Filters products based on multiple selected ratings.
        """
        if values:
            rating_queries = Q()
            for value in values:
                try:
                    value = int(value)
                    rating_queries |= Q(avg_rating__gte=value, avg_rating__lt=value + 1)
                    # include products without rating when user select 1 star
                    if value == 1:
                        rating_queries |= Q(avg_rating__isnull=True)

                except ValueError:
                    pass
            # Annotate average rating and filter
            return queryset.annotate(avg_rating=Avg("product_reviews__rating")).filter(rating_queries).order_by("avg_rating")

        return queryset

    def filter_sorting(self, queryset, name, value):
        """
        Handles sorting logic based on the 'sort' parameter.
        """
        if value == "newest":
            return queryset.order_by("-created_at")
        elif value == "popular":
            return queryset.annotate(order_count=Count("order_items")).order_by("-order_count")
        elif value == "rating":
            return queryset.annotate(avg_rating=Avg("product_reviews__rating")).order_by("-avg_rating")
        return queryset
