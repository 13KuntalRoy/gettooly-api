# Generated by Django 4.1.7 on 2023-04-20 13:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="stripe_customer_id",
        ),
        migrations.AddField(
            model_name="conductuser",
            name="stripe_customer_id",
            field=models.CharField(blank=True, default="", max_length=50),
        ),
    ]
