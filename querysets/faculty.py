# facility/querysets/faculty.py

from django.db import models
from django.db.models import Prefetch

from enrollment.models.facility import FacilityEnrollment
from enrollment.models.faculty import FacultyEnrollment


class FacultyQuerySet(models.QuerySet):
    def faculty(self):
        return self.filter(user_type="faculty")

    def by_facility(self, facility):
        return self.filter(facultyprofile__facility=facility)

    def by_organization(self, organization):
        all_organizations = [organization] + organization.get_all_children()
        return self.filter(facultyprofile__organization__in=all_organizations)

    def get_faculty_with_enrollments(self, facility_enrollment):
        return self.prefetch_related(
            Prefetch(
                'faculty_enrollments',
                queryset=FacultyEnrollment.objects.filter(facility_enrollment=facility_enrollment)
            )
        ).distinct()


class FacultyProfileQuerySet(models.QuerySet):
    def with_enrollments(self, enrollment=None, prefetch=True):
        if prefetch:
            queryset=FacultyEnrollment.objects.select_related('facility_enrollment__facility')
            if enrollment:
                queryset = queryset.filter(facility_enrollment=enrollment).distinct()
            return self.prefetch_related(
                Prefetch(
                    'enrollments',
                    queryset=queryset,
                    to_attr='prefetched_enrollments'
                )
            )
        return self.get_queryset().filter()