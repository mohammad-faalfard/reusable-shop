# Generated by Django 5.1.2 on 2024-12-16 06:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0011_alter_productwishlist_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="tags",
            field=models.ManyToManyField(blank=True, to="products.producttag", verbose_name="Tags"),
        ),
    ]
