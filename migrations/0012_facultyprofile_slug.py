# Generated by Django 5.0.6 on 2024-12-13 23:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0011_alter_facultyprofile_address_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="facultyprofile",
            name="slug",
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
