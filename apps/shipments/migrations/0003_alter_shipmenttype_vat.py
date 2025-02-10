# Generated by Django 5.1.2 on 2024-12-13 11:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shipments", "0002_alter_shipmenttype_vat"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shipmenttype",
            name="vat",
            field=models.FloatField(
                default=0,
                help_text="The VAT (Value Added Tax) percentage for this shipment type.",
                validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)],
                verbose_name="VAT",
            ),
        ),
    ]
