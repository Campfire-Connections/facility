# Generated by Django 5.0.6 on 2024-08-31 18:48

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0006_alter_facultyprofile_organization"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="facility",
            options={"verbose_name": "Facility", "verbose_name_plural": "Facilities"},
        ),
        migrations.RemoveField(
            model_name="faculty",
            name="slug",
        ),
    ]
