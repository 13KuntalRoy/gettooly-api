# Generated by Django 4.1.7 on 2023-06-15 16:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0022_alter_subscription_expires_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 7, 15, 16, 3, 54, 458530, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]