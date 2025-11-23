# facility/tables/faculty.py

import django_tables2 as tables
from core.tables.base import BaseTable

from ..models.faculty import FacultyProfile


class FacultyTable(BaseTable):
    first_name = tables.Column(accessor="user__first_name", verbose_name="First Name")
    last_name = tables.Column(accessor="user__last_name", verbose_name="Last Name")
    email = tables.Column(accessor="user__email", verbose_name="Email")
    facility = tables.Column(accessor="facility__name", verbose_name="Facility")
    role = tables.Column(accessor="get_role_display", verbose_name="Role")

    class Meta:
        model = FacultyProfile
        fields = (
            "first_name",
            "last_name",
            "email",
            "facility",
            "role",
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
