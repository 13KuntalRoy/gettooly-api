# Generated by Django 4.1.7 on 2023-04-05 08:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="expires_at",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 5, 5, 8, 39, 58, 602311, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]