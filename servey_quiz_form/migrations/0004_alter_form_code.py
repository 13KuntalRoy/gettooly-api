# Generated by Django 4.1.7 on 2023-04-04 14:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("servey_quiz_form", "0003_alter_form_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="form",
            name="code",
            field=models.CharField(
                max_length=30, unique="iDL4d8kIa5MAIDDL2dI80mUojMB7nS"
            ),
        ),
    ]
