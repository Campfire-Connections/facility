# facility/tables/faculty.py

import django_tables2 as tables
from core.tables.base import BaseTable

from user.models import User


class FacultyTable(BaseTable):
    username = tables.Column(accessor="username", verbose_name="Username")
    first_name = tables.Column(accessor="first_name", verbose_name="First Name")
    last_name = tables.Column(accessor="last_name", verbose_name="Last Name")
    email = tables.Column(accessor="email", verbose_name="Email")
    faction = tables.Column(
        accessor="facultyprofile.faction.name", verbose_name="Faction"
    )
    organization = tables.Column(
        accessor="facultyprofile.organization.name", verbose_name="Organization"
    )
    # Add more fields as needed

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "facility",
            "organization",
        )

    urls = {
        "add": {"kwargs": {"facility_slug": "facility__slug"}, "icon": "fa-user-plus"},
        "show": {
            "kwargs": {"facility_slug": "facility__slug", "quarters_slug": "slug"}
        },
        "edit": {
            "kwargs": {"facility_slug": "facility__slug", "quarters_slug": "slug"}
        },
        "delete": {
            "kwargs": {"facility_slug": "facility__slug", "quarters_slug": "slug"}
        },
    }
    url_namespace = "facilities:faculty"
