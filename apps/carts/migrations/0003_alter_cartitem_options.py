# Generated by Django 5.1.2 on 2024-11-30 10:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("carts", "0002_alter_cart_session_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cartitem",
            options={"verbose_name": "Cart Item", "verbose_name_plural": "Cart Items"},
        ),
    ]
