# facility/models/faculty.py

# from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ValidationError
from django.urls import reverse

from core.mixins import models as mixins

# from core.mixins import settings as stgs
from user.models import User, BaseUserProfile
from enrollment.models.faculty import FacultyEnrollment

# from address.models import Address
# from organization.models import Organization

from .facility import Facility
from ..managers.faculty import FacultyManager


class Faculty(
    mixins.TimestampMixin,
    mixins.SoftDeleteMixin,
    mixins.AuditMixin,
    mixins.ImageMixin,
    #  stgs.SettingsMixin,
    User,
):
    user_type = User.UserType.FACULTY
    facility = models.ForeignKey(
        "facility.Facility",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="faculty",
    )
    organization = models.ForeignKey(
        "organization.Organization",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="faculty",
    )
    # address = GenericRelation(Address, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    faculty = FacultyManager()

    class Meta:
        # proxy = True
        verbose_name = "Faculty"
        verbose_name_plural = "Faculty"

    def welcome(self):
        return "Only for faculty"

    def get_absolute_url(self):
        return reverse("faculty_show", kwargs={"faculty_slug": self.slug})

    def get_fallback_chain(self):
        return ["facility", "facility.organization"]


class FacultyProfile(BaseUserProfile):
    class Meta:
        verbose_name = "Faculty Profile"
        verbose_name_plural = "Faculty Profiles"

    facility = models.ForeignKey(
        "facility.Facility", on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def enrollments(self):
        """
        Dynamically fetch enrollments for this faculty member.
        """
        return FacultyEnrollment.objects.filter(faculty=self.user)

    def get_fallback_chain(self):
        return ["facility", "facility.organization"]


@receiver(post_save, sender=Faculty)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.user_type == "FACULTY":
        FacultyProfile.objects.create(user=instance)
