# Generated by Django 4.1.7 on 2023-05-22 07:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("servey_quiz_form", "0010_result_responder_email_alter_form_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="result",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="form",
            name="code",
            field=models.CharField(
                max_length=30, unique="BiKIpzoXrW7HkeWmFKsQk5wDacB0ul"
            ),
        ),
    ]