# facility/managers/faculty.py

from django.db import models
from django.db.models import Prefetch


from facility.querysets.faculty import FacultyProfileQuerySet
from enrollment.models.faculty import FacultyEnrollment


class FacultyManager(models.Manager):
    def get_queryset(self):
        """
        Use the custom FacultyQuerySet as the default queryset.
        """
        return FacultyProfileQuerySet(self.model, using=self._db)

    def for_facility_enrollment(self, facility_enrollment):
        return self.get_queryset().filter(
            user_type='FACULTY',
            facultyprofile_profile__facultyenrollment__facility_enrollment=facility_enrollment
        ).distinct()
