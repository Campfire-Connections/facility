from django.shortcuts import get_object_or_404

from core.policies import visible_facilities_for_user
from course.models.facility_class import FacilityClass
from course.tables.facility_class import FacilityClassTable
from enrollment.models.facility import FacilityEnrollment
from enrollment.tables.facility import FacilityEnrollmentTable
from facility.models.department import Department
from facility.models.facility import Facility
from facility.models.faculty import FacultyProfile
from facility.models.quarters import Quarters
from facility.tables.department import DepartmentTable
from facility.tables.facility import FacilityTable
from facility.tables.faculty import FacultyTable
from facility.tables.quarters import QuartersTable


def facility_list_queryset(user=None):
    if user is not None:
        return visible_facilities_for_user(user)
    return Facility.objects.all()


def facility_queryset_for_organization(organization):
    return Facility.objects.filter(organization=organization)


def get_facility_by_slug(slug):
    return get_object_or_404(Facility, slug=slug)


def departments_for_facility(facility):
    return Department.objects.filter(facility=facility)


def quarters_for_facility(facility):
    return Quarters.objects.filter(facility=facility)


def faculty_for_facility(facility):
    return FacultyProfile.objects.filter(facility=facility).select_related("user")


def classes_for_facility(facility):
    return FacilityClass.objects.filter(facility_enrollment__facility=facility)


def enrollments_for_facility(facility):
    return FacilityEnrollment.objects.filter(facility=facility)


def facility_manage_tables_config(facility):
    context = {"facility_slug": facility.slug}
    return {
        "departments": {
            "class": DepartmentTable,
            "queryset": departments_for_facility(facility),
            "paginate_by": 6,
            "context": context,
        },
        "quarters": {
            "class": QuartersTable,
            "queryset": quarters_for_facility(facility),
            "paginate_by": 6,
            "context": context,
        },
        "faculty": {
            "class": FacultyTable,
            "queryset": faculty_for_facility(facility),
            "paginate_by": 6,
            "context": context,
        },
        "facility_classes": {
            "class": FacilityClassTable,
            "queryset": classes_for_facility(facility),
            "paginate_by": 6,
            "context": context,
        },
        "facility_enrollments": {
            "class": FacilityEnrollmentTable,
            "queryset": enrollments_for_facility(facility),
            "paginate_by": 6,
            "context": context,
        },
    }


def facility_detail_tables_config(facility):
    return {
        "departments_table": {
            "class": DepartmentTable,
            "queryset": departments_for_facility(facility),
        },
        "quarters_table": {
            "class": QuartersTable,
            "queryset": quarters_for_facility(facility),
        },
        "faculty_table": {
            "class": FacultyTable,
            "queryset": faculty_for_facility(facility),
        },
        "facility_enrollment_table": {
            "class": FacilityEnrollmentTable,
            "queryset": enrollments_for_facility(facility),
        },
    }
