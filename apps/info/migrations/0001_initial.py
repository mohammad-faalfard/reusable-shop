# Generated by Django 5.1.2 on 2024-11-08 13:23

import django.contrib.gis.db.models.fields
import django.core.validators
import django.db.models.deletion
import django_lifecycle.mixins
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutUs",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                (
                    "text",
                    models.TextField(
                        help_text="Maximum 1000 characters",
                        validators=[django.core.validators.MaxLengthValidator(1000)],
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
                "verbose_name": "About Us",
                "verbose_name_plural": "About Us Entries",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="FAQGroup",
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
                "verbose_name": "FAQ Group",
                "verbose_name_plural": "FAQ Groups",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="FAQ",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
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
                (
                    "logo",
                    models.ImageField(
                        blank=True,
                        help_text="An optional logo image for the FAQ.",
                        null=True,
                        upload_to="faq_logos/",
                        verbose_name="Logo",
                    ),
                ),
                (
                    "answer",
                    models.TextField(
                        help_text="Maximum 500 characters",
                        validators=[django.core.validators.MaxLengthValidator(500)],
                        verbose_name="Answer",
                    ),
                ),
                (
                    "faq_group",
                    models.ForeignKey(
                        help_text="The group to which this FAQ belongs.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="faqs",
                        to="info.faqgroup",
                        verbose_name="FAQ Group",
                    ),
                ),
            ],
            options={
                "verbose_name": "FAQ",
                "verbose_name_plural": "FAQs",
            },
        ),
        migrations.CreateModel(
            name="PrivacyPolicy",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                (
                    "text",
                    models.TextField(
                        help_text="Maximum 5000 characters",
                        validators=[django.core.validators.MaxLengthValidator(5000)],
                        verbose_name="Privacy Policy Text",
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
                "verbose_name": "Privacy Policy",
                "verbose_name_plural": "Privacy Policies",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ShopLocation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                (
                    "address",
                    models.CharField(
                        help_text="The physical address of the shop location.", max_length=200, verbose_name="Address"
                    ),
                ),
                (
                    "location",
                    django.contrib.gis.db.models.fields.PointField(
                        help_text="Geographical coordinates (longitude, latitude) of the shop location.",
                        srid=4326,
                        verbose_name="Location",
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
                "verbose_name": "Shop Location",
                "verbose_name_plural": "Shop Locations",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="State",
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
                ("title", models.CharField(max_length=100, unique=True, verbose_name="Title")),
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
                "verbose_name": "State",
                "verbose_name_plural": "States",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name="Created At")),
                ("updated_at", models.DateTimeField(auto_now=True, null=True, verbose_name="Updated at")),
                ("is_active", models.BooleanField(db_index=True, default=True, verbose_name="Is active")),
                ("title", models.CharField(max_length=100, verbose_name="Title")),
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
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cities",
                        to="info.state",
                        verbose_name="State",
                    ),
                ),
            ],
            options={
                "verbose_name": "City",
                "verbose_name_plural": "Cities",
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
