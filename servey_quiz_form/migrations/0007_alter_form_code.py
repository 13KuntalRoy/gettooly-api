# Generated by Django 4.1.7 on 2023-04-20 13:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("servey_quiz_form", "0006_alter_form_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="form",
            name="code",
            field=models.CharField(
                max_length=30, unique="x1dzAtkbUL1MXA8IlOzudU2lzOjX62"
            ),
        ),
    ]