# Generated by Django 4.1.7 on 2023-04-14 11:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0003_alter_subscription_expires_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 5, 14, 11, 32, 41, 750706, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]