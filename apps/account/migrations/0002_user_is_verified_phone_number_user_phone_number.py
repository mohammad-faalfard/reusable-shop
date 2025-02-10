# Generated by Django 5.0.2 on 2024-07-03 20:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]
    operations = [
        migrations.AddField(
            model_name="user",
            name="is_verified_phone_number",
            field=models.BooleanField(default=False, verbose_name="Is Verified Phone Number"),
        ),
        migrations.AddField(
            model_name="user",
            name="phone_number",
            field=models.CharField(max_length=14, null=True, unique=True, verbose_name="Phone Number"),
        ),
    ]
