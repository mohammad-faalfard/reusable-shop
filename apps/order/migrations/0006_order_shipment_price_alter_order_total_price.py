# Generated by Django 5.1.2 on 2024-12-13 14:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0005_alter_order_coupon_total_discount_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="shipment_price",
            field=models.FloatField(default=0, help_text="The shipment price", verbose_name="Shipment Price"),
        ),
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.FloatField(
                help_text="The final total price after all discounts (both product and coupon discounts) have been applied and shipment price.",
                verbose_name="Total Price",
            ),
        ),
    ]
