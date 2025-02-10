# Generated by Django 5.1.2 on 2024-11-30 10:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("carts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="session_id",
            field=models.CharField(
                blank=True, db_index=True, max_length=64, null=True, unique=True, verbose_name="Session ID"
            ),
        ),
    ]
