# Generated by Django 5.1.2 on 2024-12-14 09:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0008_remove_productreview_title"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="productreview",
            name="unique_product_review_per_user",
        ),
    ]
