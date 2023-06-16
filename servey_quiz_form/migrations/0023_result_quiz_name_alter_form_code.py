# Generated by Django 4.1.7 on 2023-06-15 16:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("servey_quiz_form", "0022_alter_form_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="result",
            name="quiz_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="form",
            name="code",
            field=models.CharField(
                max_length=30, unique="ZsZ7m2KhmiouQVedOKk58zpZvIPhyO"
            ),
        ),
    ]