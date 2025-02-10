# Generated by Django 5.1.2 on 2024-11-15 15:03

import django.core.validators
import django.db.models.deletion
import django_lifecycle.mixins
import django_resized.forms
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductCategory",
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
                ("logo", models.ImageField(upload_to="category_logos/", verbose_name="Logo")),
                (
                    "description",
                    models.TextField(
                        help_text="Maximum 3000 characters",
                        validators=[django.core.validators.MaxLengthValidator(3000)],
                        verbose_name="Description",
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
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="products.productcategory",
                        verbose_name="Parent",
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
                "verbose_name": "Product Category",
                "verbose_name_plural": "Product Categories",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                ("title", models.CharField(max_length=100, verbose_name="Title")),
                ("stock", models.PositiveIntegerField(verbose_name="Stock")),
                (
                    "description",
                    models.TextField(
                        help_text="Maximum 3000 characters",
                        validators=[django.core.validators.MaxLengthValidator(3000)],
                        verbose_name="Description",
                    ),
                ),
                (
                    "price",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(999999999),
                        ],
                        verbose_name="Price",
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
                ("variants", models.ManyToManyField(blank=True, to="products.product", verbose_name="Variants")),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="products.productcategory",
                        verbose_name="Category",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ProductDiscount",
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
                ("type", models.PositiveSmallIntegerField(choices=[(0, "Percent"), (1, "Amount")], verbose_name="Type")),
                ("amount", models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name="Amount")),
                ("active_from", models.DateTimeField(blank=True, null=True, verbose_name="Active From")),
                ("active_until", models.DateTimeField(blank=True, null=True, verbose_name="Active Until")),
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
                "verbose_name": "Product Discount",
                "verbose_name_plural": "Product Discounts",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ProductImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                (
                    "image",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format="WEBP",
                        keep_meta=True,
                        null=True,
                        quality=100,
                        scale=1,
                        size=[1920, 1080],
                        upload_to="products/images/",
                        verbose_name="Image",
                    ),
                ),
                ("alt_text", models.CharField(blank=True, max_length=100, verbose_name="Alt Text")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_images",
                        to="products.product",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Image",
                "verbose_name_plural": "Product Images",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ProductReview",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                ("title", models.CharField(max_length=100, verbose_name="Title")),
                (
                    "text",
                    models.TextField(
                        help_text="Maximum 500 characters",
                        validators=[django.core.validators.MaxLengthValidator(500)],
                        verbose_name="Text",
                    ),
                ),
                (
                    "rating",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Poor"), (2, "Average"), (3, "Good"), (4, "Very Good"), (5, "Excellent")],
                        default=5,
                        verbose_name="Rating",
                    ),
                ),
                ("is_accepted", models.BooleanField(default=False, verbose_name="Is Accepted")),
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
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="product_review",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Review",
                "verbose_name_plural": "Product Reviews",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ProductTag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                ("title", models.CharField(max_length=100, verbose_name="Title")),
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
                "verbose_name": "Product Tag",
                "verbose_name_plural": "Product Tags",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ProductWishlist",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="products.product", verbose_name="Product"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_wish_list",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Wishlist",
                "verbose_name_plural": "Product Wishlists",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ProductProperty",
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
                ("value", models.CharField(max_length=100, verbose_name="Value")),
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
                "verbose_name": "Product Property",
                "verbose_name_plural": "Product Properties",
                "unique_together": {("product", "title", "value")},
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
