# Generated by Django 4.1.7 on 2023-06-14 11:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("servey_quiz_form", "0021_alter_form_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="form",
            name="code",
            field=models.CharField(
                max_length=30, unique="b3eQLYmJrJQU5vvTO0EvfjbtKzcxDB"
            ),
        ),
    ]