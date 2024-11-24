# facility/views/facility.py

from django.urls import reverse_lazy
from django.views.generic import (
    ListView as _ListView,
    CreateView as _CreateView,
    UpdateView as _UpdateView,
    DeleteView as _DeleteView,
    DetailView as _DetailView,
)
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView
from django_tables2 import MultiTableMixin, SingleTableView
from django_tables2.config import RequestConfig

from organization.models.organization import Organization
from enrollment.models.facility import FacilityEnrollment
from enrollment.tables.facility import FacilityEnrollmentTable
from course.models.facility_class import FacilityClass
from course.tables.facility_class import FacilityClassTable
from user.models import User
from core.views.base import BaseManageView
from ..models.facility import Facility
from ..models.department import Department
from ..models.quarters import Quarters
from ..forms.facility import FacilityForm
from ..tables.facility import FacilityTable
from ..tables.department import DepartmentTable
from ..tables.quarters import QuartersTable
from ..tables.faculty import FacultyTable

class IndexView(SingleTableView):
    model = Facility
    template_name = "facility/index.html"
    table_class = FacilityTable
    context_object_name = "facilities"


class IndexByOrganizationView(_ListView):
    model = Facility
    template_name = "facility/index.html"
    context_object_name = "facilities"

    def get_queryset(self):
        # Allow lookup by pk or slug
        organization_lookup = self.kwargs.get("organization_pk") or self.kwargs.get(
            "organization_slug"
        )

        # Check if the lookup is a digit (assume it's a pk if so)
        if organization_lookup.isdigit():
            organization = get_object_or_404(Organization, pk=organization_lookup)
        else:
            organization = get_object_or_404(Organization, slug=organization_lookup)

        return Facility.objects.filter(organization=organization)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization_lookup = self.kwargs.get("organization_pk") or self.kwargs.get(
            "organization_slug"
        )

        if organization_lookup.isdigit():
            organization = get_object_or_404(Organization, pk=organization_lookup)
        else:
            organization = get_object_or_404(Organization, slug=organization_lookup)

        context["organization"] = organization
        return context


class ManageView(LoginRequiredMixin, UserPassesTestMixin, BaseManageView):
    template_name = "facility/manage.html"

    def get_facility(self):
        """
        Get the facility associated with the current user.
        """
        user = self.request.user
        profile = user.facultyprofile
        return get_object_or_404(Facility, id=profile.facility_id)

    def get_tables_config(self):
        """
        Define tables for the manage view with their querysets and pagination.
        """
        facility = self.get_facility()
        return {
            "departments": {
                "class": DepartmentTable,
                "queryset": Department.objects.filter(facility=facility),
                "paginate_by": 6,
            },
            "facility_classes": {
                "class": FacilityClassTable,
                "queryset": FacilityClass.objects.filter(facility_enrollment__facility=facility),
                "paginate_by": 6,
            },
            "facility_enrollments": {
                "class": FacilityEnrollmentTable,
                "queryset": FacilityEnrollment.objects.filter(facility=facility),
                "paginate_by": 6,
            },
        }

    def test_func(self):
        """
        Check if the user is a faculty member with admin privileges.
        """
        return self.request.user.user_type == "FACULTY" and self.request.user.is_admin
class ShowView(_DetailView):
    model = Facility
    template_name = "facility/show.html"
    context_object_name = "facility"
    slug_field = "slug"
    slug_url_kwarg = "facility_slug"

    def get_context_data(self, **kwargs):
        """
        Add tables of related data for departments, quarters (filtered by quarters_type),
        faculty, and facility enrollments.
        """
        context = super().get_context_data(**kwargs)
        facility = self.get_object()

        # Fetch related data
        departments = Department.objects.filter(facility=facility)
        # faculty_type = QuartersType.objects.get(name='faculty')
        quarters = Quarters.objects.filter(facility=facility)  # , type=faculty_type)
        faculty = User.objects.filter(
            user_type="FACULTY", facultyprofile__facility=facility
        ).select_related("facultyprofile")
        facility_enrollments = FacilityEnrollment.objects.filter(facility=facility)

        # Initialize tables
        department_table = DepartmentTable(departments)
        quarters_table = QuartersTable(quarters)
        faculty_table = FacultyTable(faculty)
        facility_enrollment_table = FacilityEnrollmentTable(facility_enrollments)

        # Configure tables with request context for pagination, sorting, etc.
        RequestConfig(self.request).configure(department_table)
        RequestConfig(self.request).configure(quarters_table)
        RequestConfig(self.request).configure(faculty_table)
        RequestConfig(self.request).configure(facility_enrollment_table)

        # Add tables to context
        context["departments_table"] = department_table
        context["quarters_table"] = quarters_table
        context["faculty_table"] = faculty_table
        context["facility_enrollment_table"] = facility_enrollment_table

        return context


class CreateView(_CreateView):
    model = Facility
    form_class = FacilityForm
    template_name = "facility/form.html"
    success_url = reverse_lazy("facility_index")


class UpdateView(_UpdateView):
    model = Facility
    form_class = FacilityForm
    template_name = "facility/form.html"
    success_url = reverse_lazy("facility_index")


class DeleteView(_DeleteView):
    model = Facility
    template_name = "facility/confirm_delete.html"
    success_url = reverse_lazy("facility_index")
