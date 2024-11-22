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
from enrollment.models.organization import OrganizationCourse
from enrollment.models.temporal import Week, Period
from enrollment.models.facility import FacilityEnrollment
from enrollment.tables.facility import FacilityEnrollmentTable
from course.models.facility_class import FacilityClass
from course.tables.facility_class import FacilityClassTable
from user.models import User
from ..models.facility import Facility
from ..models.department import Department
from ..models.quarters import Quarters, QuartersType
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


class ManageView(
    LoginRequiredMixin, UserPassesTestMixin, MultiTableMixin, TemplateView
):
    template_name = "facility/manage.html"

    def get_tables(self):
        """
        Retrieves and configures tables for departments, facility classes, and facility enrollments
        associated with a specific facility. This function constructs querysets, builds tables, and
        applies pagination and sorting configurations.

        Args:
            self: The instance of the class.

        Returns:
            list: A list containing the configured tables for departments, facility classes, and 
            facility enrollments.
        """

        facility = self.get_facility()

        # Construct querystrings
        departments_qs = Department.objects.filter(facility=facility)
        facility_classes_qs = FacilityClass.objects.filter(
            facility_enrollment__facility=facility
        )
        facility_enrollments_qs = FacilityEnrollment.objects.filter(facility=facility)

        # Build tables with querystrings
        department_table = DepartmentTable(departments_qs)
        facility_class_table = FacilityClassTable(facility_classes_qs)
        facility_enrollment_table = FacilityEnrollmentTable(
            facility_enrollments_qs, user=self.request.user
        )

        # Configure tables with pagination and sorting
        RequestConfig(self.request, paginate={"per_page": 6}).configure(
            facility_class_table
        )
        RequestConfig(self.request, paginate={"per_page": 6}).configure(
            department_table
        )
        RequestConfig(self.request, paginate={"per_page": 6}).configure(
            facility_enrollment_table
        )

        return [
            department_table,
            facility_class_table,
            facility_enrollment_table,
        ]

    def get_context_data(self, **kwargs):
        """
        Constructs and returns the context data for rendering a template, including various tables 
        and related entities for a specific facility. This function enhances the context with 
        additional information such as departments, classes, enrollments, and other related data.

        Args:
            self: The instance of the class.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the context data for the template, including tables with 
                names and various related entities.
        """

        context = super().get_context_data(**kwargs)
        facility = self.get_facility()

        tables_with_names = [
            {
                "table": table,
                "name": table.Meta.model._meta.verbose_name_plural,
                "create_url": table.get_url(
                    "add", context={"facility_slug": facility.slug}
                ),
                "icon": getattr(table, "add_icon", None),
            }
            for table in self.get_tables()
        ]
        context.update(
            {
                "tables_with_names": tables_with_names,
                "facility": facility,
                # "departments": Department.objects.filter(facility=facility),
                # "quarters": Quarters.objects.filter(facility=facility),
                # "classes": FacilityClass.objects.filter(
                #     facility_enrollment__facility=facility
                # ),
                # "enrollments": FacilityEnrollment.objects.filter(facility=facility),
                # "courses": OrganizationCourse.objects.filter(
                #     organization_enrollment__organization=facility.organization
                # ),
                # "weeks": Week.objects.filter(facility_enrollment__facility=facility),
                # "periods": Period.objects.filter(
                #     week__facility_enrollment__facility=facility
                # ),
            }
        )

        return context

    def get_facility(self):
        user = self.request.user
        profile = user.facultyprofile
        return get_object_or_404(Facility, id=profile.facility_id)

    def test_func(self):
        # Check if the user is a faculty member with admin privileges
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
