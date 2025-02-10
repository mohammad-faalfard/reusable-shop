# Generated by Django 5.1.2 on 2024-11-16 17:35

import django.core.validators
import django.db.models.deletion
import django_lifecycle.mixins
import django_resized.forms
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("products", "0003_productreview_unique_product_review_per_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductOffer",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                ("title", models.CharField(max_length=100, verbose_name="Title")),
                ("active_from", models.DateTimeField(db_index=True, verbose_name="Active From")),
                ("active_until", models.DateTimeField(db_index=True, verbose_name="Active Until")),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Offer",
                "verbose_name_plural": "Product Offers",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Slider",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                (
                    "priority",
                    models.PositiveSmallIntegerField(
                        db_index=True,
                        default=0,
                        help_text="Priority of the record. Starting from 0",
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Priority",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Title")),
                ("media", models.FileField(upload_to="media/uploads/", verbose_name="Media")),
                ("link", models.CharField(blank=True, max_length=255, null=True, verbose_name="Link")),
                ("sub_title", models.CharField(max_length=100, verbose_name="Subtitle")),
                ("button_text", models.CharField(blank=True, max_length=100, null=True, verbose_name="Button Text")),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Slider",
                "verbose_name_plural": "Sliders",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Banner",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                ("title", models.CharField(max_length=100, verbose_name="Title")),
                (
                    "image",
                    django_resized.forms.ResizedImageField(
                        crop=None,
                        force_format="WEBP",
                        keep_meta=True,
                        quality=100,
                        scale=1,
                        size=[1920, 1080],
                        upload_to="banner/images/",
                        verbose_name="Image",
                    ),
                ),
                (
                    "link",
                    models.URLField(
                        blank=True, help_text="Optional link to associate with the banner.", null=True, verbose_name="Link"
                    ),
                ),
                ("text", models.TextField(verbose_name="Text")),
                ("button_text", models.CharField(blank=True, max_length=100, null=True, verbose_name="Button Text")),
                (
                    "holder",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Main Page - First"), (1, "Main Page - Second")],
                        help_text="Placement of the banner in the frontend.",
                        verbose_name="Holder",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Banner",
                "verbose_name_plural": "Banners",
                "constraints": [models.UniqueConstraint(fields=("holder", "is_active"), name="unique_holder_is_active")],
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ProductOfferItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                ("stock", models.PositiveIntegerField(blank=True, db_index=True, null=True, verbose_name="Stock")),
                (
                    "discount",
                    models.FloatField(
                        db_index=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Discount"
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Created By",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="products.product", verbose_name="Product"
                    ),
                ),
                (
                    "product_offer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offer_items",
                        to="cms.productoffer",
                        verbose_name="Product Offer",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated_by",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Offer Item",
                "verbose_name_plural": "Product Offer Items",
                "constraints": [models.UniqueConstraint(fields=("product",), name="unique_product_offer_item")],
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
