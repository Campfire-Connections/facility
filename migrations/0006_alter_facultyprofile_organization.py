# Generated by Django 5.0.6 on 2024-08-18 16:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0005_facultyprofile_address_alter_facility_address"),
        ("organization", "0002_alter_organization_description_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="facultyprofile",
            name="organization",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="organization.organization",
            ),
            preserve_default=False,
        ),
    ]
