# facility/tables/faculty.py

import django_tables2 as tables
from core.tables.base import BaseTable

from ..models.faculty import FacultyProfile


class FacultyTable(BaseTable):
    first_name = tables.Column(accessor="user.first_name", verbose_name="First Name")
    last_name = tables.Column(accessor="user.last_name", verbose_name="Last Name")
    email = tables.Column(accessor="user.email", verbose_name="Email")
    facility = tables.Column(accessor="facility.name", verbose_name="Facility")

    class Meta:
        model = FacultyProfile
        fields = (
            "first_name",
            "last_name",
            "email",
            "facility",
        )

    urls = {
        "add": {
            "kwargs": {
                "facility_slug": "facility__slug"
            },
            "icon": "fa-user-plus",
        },
        "show": {
            "kwargs": {
                "facility_slug": "facility__slug",
                "faculty_slug": "slug",
            }
        },
        "edit": {
            "kwargs": {
                "facility_slug": "facility__slug",
                "faculty_slug": "slug",
            }
        },
        "delete": {
            "kwargs": {
                "facility_slug": "facility__slug",
                "faculty_slug": "slug",
            }
        },
    }
    url_namespace = "facilities:faculty"

class FacultyByFacilityTable(FacultyTable):
    class Meta(FacultyTable.Meta):
        pass
