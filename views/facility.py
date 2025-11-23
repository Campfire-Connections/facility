# facility/views/facility.py

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.views.generic import TemplateView

from core.views.base import (
    BaseManageView,
    BaseIndexByFilterTableView,
    BaseCreateView,
    BaseDeleteView,
    BaseDetailWithTablesView,
    BaseTableListView,
    BaseUpdateView,
    BaseDashboardView,
)
from core.mixins.views import (
    FacilityScopedMixin,
    OrgScopedMixin,
    PortalPermissionMixin,
)

from organization.models.organization import Organization
from enrollment.models.facility import FacilityEnrollment
from enrollment.tables.facility import FacilityEnrollmentTable
from course.models.facility_class import FacilityClass
from course.tables.facility_class import FacilityClassTable

from ..models.facility import Facility
from ..models.faculty import FacultyProfile
from ..forms.facility import FacilityForm
from ..tables.facility import FacilityTable
from ..models.department import Department
from ..tables.department import DepartmentTable
from ..models.quarters import Quarters
from ..tables.quarters import QuartersTable
from ..tables.faculty import FacultyTable

from core.dashboard_data import get_facility_metrics, get_facility_overview_text


class IndexView(BaseTableListView):
    """
    Table of facilities.
    """

    model = Facility
    template_name = "facility/list.html"
    table_class = FacilityTable
    context_object_name = "facilities"


class IndexByOrganizationView(OrgScopedMixin, BaseIndexByFilterTableView):
    """
    Facilities filtered by organization (pk or slug).
    """

    model = Facility
    template_name = "facility/list.html"
    context_object_name = "facilities"
    table_class = FacilityTable

    lookup_keys = ["organization_slug", "organization_pk"]
    filter_field = "organization"
    filter_model = Organization
    context_object_name_for_filter = "organization"


class ManageView(PortalPermissionMixin, FacilityScopedMixin, BaseManageView):
    """
    Manage view for a facility: departments, classes, enrollments etc.
    """

    template_name = "facility/manage.html"
    portal_key = "facility"

    def get_facility(self):
        facility = self.get_scope_facility()
        if facility:
            return facility
        user = self.request.user
        profile = getattr(user, "facultyprofile_profile", None)
        if profile and profile.facility_id:
            return get_object_or_404(Facility, id=profile.facility_id)
        raise Http404("Facility not found for user")

    def get_tables_config(self):
        facility = self.get_facility()
        return {
            "departments": {
                "class": DepartmentTable,
                "queryset": Department.objects.filter(facility=facility),
                "paginate_by": 6,
            },
            "facility_classes": {
                "class": FacilityClassTable,
                "queryset": FacilityClass.objects.filter(
                    facility_enrollment__facility=facility
                ),
                "paginate_by": 6,
            },
            "facility_enrollments": {
                "class": FacilityEnrollmentTable,
                "queryset": FacilityEnrollment.objects.filter(facility=facility),
                "paginate_by": 6,
            },
        }

    def get_create_url(self, table):
        facility = self.get_facility()
        # Tables are expected to have a get_url helper
        return table.get_url("add", context={"facility_slug": facility.slug})

    def get_context_data(self, **kwargs):
        # Avoid MultiTableMixin's self.tables requirement; build from config instead.
        context = TemplateView.get_context_data(self, **kwargs)
        tables = self.build_tables()
        formatted = []
        for table in tables.values():
            formatted.append(
                {
                    "table": table,
                    "name": table.Meta.model._meta.verbose_name.title(),
                    "create_url": getattr(table, "add_url", None),
                    "icon": getattr(table, "add_icon", None),
                }
            )

        facility = self.get_facility()
        context.update(
            scope_object=facility,
            facility=facility,
            tables_with_names=formatted,
        )
        return context


class ShowView(FacilityScopedMixin, BaseDetailWithTablesView):
    """
    Detailed facility view with several related tables rendered below it.
    """

    model = Facility
    template_name = "facility/show.html"
    context_object_name = "facility"
    object_slug_kwarg = "facility_slug"  # For BaseSlugOrPkObjectMixin inside BaseDetailWithTablesView

    def get_tables_config(self):
        facility = self.get_object()
        return {
            "departments_table": {
                "class": DepartmentTable,
                "queryset": Department.objects.filter(facility=facility),
            },
            "quarters_table": {
                "class": QuartersTable,
                "queryset": Quarters.objects.filter(facility=facility),
            },
            "faculty_table": {
                "class": FacultyTable,
                "queryset": FacultyProfile.objects.filter(
                    facility=facility
                ).select_related("user"),
            },
            "facility_enrollment_table": {
                "class": FacilityEnrollmentTable,
                "queryset": FacilityEnrollment.objects.filter(facility=facility),
            },
        }


class CreateView(BaseCreateView):
    """
    Create a facility.
    """

    model = Facility
    form_class = FacilityForm
    template_name = "facility/form.html"
    success_url = reverse_lazy("facilities:index")


class UpdateView(BaseUpdateView):
    """
    Update a facility.
    """

    model = Facility
    form_class = FacilityForm
    template_name = "facility/form.html"
    success_url = reverse_lazy("facilities:index")


class DeleteView(BaseDeleteView):
    """
    Confirm + delete (or soft-delete) a facility.
    """

    model = Facility
    template_name = "facility/confirm_delete.html"
    success_url = reverse_lazy("facilities:index")


class DashboardView(PortalPermissionMixin, FacilityScopedMixin, BaseDashboardView):
    """
    Dashboard for faculty members at a facility.
    """

    template_name = "faculty/dashboard.html"
    portal_key = "facility"

    def get_facility_metrics_widget(self, _definition):
        facility = self.get_scope_facility()
        metrics = get_facility_metrics(facility)
        if not metrics:
            return None
        return {"metrics": metrics}

    def get_facility_overview_widget(self, _definition):
        facility = self.get_scope_facility()
        return {"content": get_facility_overview_text(facility)}
