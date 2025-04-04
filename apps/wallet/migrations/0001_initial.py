# Generated by Django 5.0.2 on 2024-07-03 20:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Wallet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created At")),
                ("title", models.CharField(blank=True, default=True, max_length=50, verbose_name="title")),
                ("current_balance", models.BigIntegerField(default=0, verbose_name="current balance")),
            ],
            options={
                "verbose_name": "wallet",
                "verbose_name_plural": "wallets",
            },
        ),
        migrations.CreateModel(
            name="WalletTransaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Created At")),
                ("value", models.BigIntegerField(default=0, verbose_name="value")),
                ("log", models.CharField(blank=True, default="", max_length=50, verbose_name="log")),
                ("total_balance", models.BigIntegerField(default=0, verbose_name="total balance")),
                (
                    "wallet",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="wallet.wallet", verbose_name="wallet"),
                ),
            ],
            options={
                "verbose_name": "wallet transaction",
                "verbose_name_plural": "wallet transactions",
            },
        ),
    ]
