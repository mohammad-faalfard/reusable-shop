# Generated by Django 5.1.2 on 2024-12-11 19:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_productdiscount_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="views_count",
            field=models.IntegerField(blank=True, default=0, editable=False, verbose_name="view count"),
        ),
    ]
