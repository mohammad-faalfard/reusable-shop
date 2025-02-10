# Generated by Django 5.1.2 on 2024-12-14 17:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogs", "0003_alter_post_category"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogbookmark",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="blog_bookmarks",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]
