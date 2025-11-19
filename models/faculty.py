# facility/models/faculty.py

from django.db import models

from user.models import BaseUserProfile
from enrollment.models.faculty import FacultyEnrollment


class FacultyProfile(BaseUserProfile):
    class Meta:
        verbose_name = "Faculty Profile"
        verbose_name_plural = "Faculty Profiles"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "slug"],
                name="unique_faculty_slug_per_org",
            ),
            models.UniqueConstraint(
                fields=["facility", "user"],
                name="unique_faculty_per_facility_user",
            ),
        ]

    facility = models.ForeignKey(
        "facility.Facility", on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def enrollments(self):
        """
        Dynamically fetch enrollments for this faculty member.
        """
        return FacultyEnrollment.objects.filter(faculty=self)

    def get_fallback_chain(self):
        return ["facility", "facility.organization"]
