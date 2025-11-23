# facility/models/faculty.py

from django.db import models

from user.models import BaseUserProfile
from enrollment.models.faculty import FacultyEnrollment


class FacultyProfile(BaseUserProfile):
    class FacultyRole(models.TextChoices):
        ADMIN = "ADMIN", "Facility Admin"
        DEPARTMENT_ADMIN = "DEPARTMENT_ADMIN", "Department Admin"
        STAFF = "STAFF", "Faculty"

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

    role = models.CharField(
        max_length=32,
        choices=FacultyRole.choices,
        default=FacultyRole.STAFF,
    )
    department = models.ForeignKey(
        "facility.Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faculty",
    )
    facility = models.ForeignKey(
        "facility.Facility", on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def is_facility_admin(self):
        return self.role == self.FacultyRole.ADMIN

    @property
    def is_department_admin(self):
        return self.role in (
            self.FacultyRole.ADMIN,
            self.FacultyRole.DEPARTMENT_ADMIN,
        )

    @property
    def enrollments(self):
        """
        Dynamically fetch enrollments for this faculty member.
        """
        return FacultyEnrollment.objects.filter(faculty=self)

    def get_root_organization(self):
        """Return the root organization for this faculty member."""
        if self.organization:
            return self.organization.get_root_organization()
        return None

    def get_fallback_chain(self):
        return ["facility", "facility.organization"]

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("facilities:faculty:show", kwargs={"faculty_slug": self.slug})
