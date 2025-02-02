# facility/tables/faculty.py

import django_tables2 as tables
from core.tables.base import BaseTable

from user.models import User


class FacultyTable(BaseTable):
    #first_name = tables.Column(accessor="user__first_name", verbose_name="First Name")
    #last_name = tables.Column(accessor="user__last_name", verbose_name="Last Name")
    #email = tables.Column(accessor="user__email", verbose_name="Email")
    #facility = tables.Column(accessor="facultyprofile_profile__facility.name", verbose_name="Facility")
    # organization = tables.Column(
    #     accessor="facultyprofile_profile.organization.name", verbose_name="Organization"
    # )
    # Add more fields as needed

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            #"email",
            #"facility",
            #"organization",
        )

    urls = {
        "add": {
            "kwargs": {
                "facility_slug": "facultyprofile_profile__facility__slug"
            },
            "icon": "fa-user-plus",
        },
        "show": {
            "kwargs": {
                "facility_slug": "facultyprofile_profile__facility__slug",
                "faculty_slug": "facultyprofile_profile__slug",
            }
        },
        "edit": {
            "kwargs": {
                "facility_slug": "facultyprofile_profile__facility__slug",
                "faculty_slug": "facultyprofile_profile__slug",
            }
        },
        "delete": {
            "kwargs": {
                "facility_slug": "facultyprofile_profile__facility__slug",
                "faculty_slug": "facultyprofile_profile__slug",
            }
        },
    }
    url_namespace = "facilities:faculty"

class FacultyByFacilityTable(FacultyTable):
    class Meta(FacultyTable.Meta):
        pass