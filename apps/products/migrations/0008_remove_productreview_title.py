# Generated by Django 5.1.2 on 2024-12-14 06:53

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0007_product_views_count"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productreview",
            name="title",
        ),
    ]
