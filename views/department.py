# facility/views/department.py

from django.urls import reverse, reverse_lazy
from django import forms
from django.shortcuts import get_object_or_404

from core.views.base import (
    BaseIndexByFilterTableView,
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseTableListView,
    BaseUpdateView,
    BaseSlugOrPkObjectMixin,
)
from ..models.facility import Facility
from ..models.department import Department
from ..forms.department import DepartmentForm
from ..tables.department import DepartmentTable


class IndexView(BaseTableListView):
    """
    Table listing of all departments.
    """

    model = Department
    template_name = "department/list.html"
    table_class = DepartmentTable
    context_object_name = "departments"


class IndexByFacilityView(BaseIndexByFilterTableView):
    """
    Departments filtered by facility (facility_slug or facility_pk).
    """

    model = Department
    template_name = "department/list.html"
    context_object_name = "departments"
    table_class = DepartmentTable

    lookup_keys = ["facility_slug", "facility_pk"]
    filter_field = "facility"
    filter_model = Facility
    context_object_name_for_filter = "facility"


class ShowView(BaseSlugOrPkObjectMixin, BaseDetailView):
    """
    Department detail view that can use either pk or slug.
    """

    model = Department
    template_name = "department/show.html"
    context_object_name = "department"

    object_pk_kwarg = "department_id"
    object_slug_kwarg = "department_slug"


class CreateView(BaseCreateView):
    """
    Create a Department under a specific Facility (by facility_slug).
    Facility is pre-populated and hidden in the form.
    """

    model = Department
    form_class = DepartmentForm
    template_name = "department/form.html"

    def get_success_url(self):
        facility_slug = self.kwargs.get("facility_slug")
        return reverse(
            "facilities:departments:show",
            kwargs={
                "facility_slug": facility_slug,
                "department_slug": self.object.slug,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # organization_labels from session for dynamic naming
        labels = self.request.session.get("organization_labels", {})
        context["title"] = labels.get("department_label", "Department")

        return context

    def get_initial(self):
        initial = super().get_initial()
        facility_slug = self.kwargs.get("facility_slug")

        try:
            facility = Facility.objects.get(slug=facility_slug)
            initial["facility"] = facility
        except Facility.DoesNotExist:
            pass

        return initial

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        facility_slug = self.kwargs.get("facility_slug")

        if facility_slug:
            try:
                facility = Facility.objects.get(slug=facility_slug)
                form.fields["facility"].initial = facility
                form.fields["facility"].widget = forms.HiddenInput()
                form.fields["facility"].label = None
            except Facility.DoesNotExist:
                pass

        return form


class UpdateView(BaseUpdateView):
    """
    Update a Department, identified by slug in the URL.
    """

    model = Department
    form_class = DepartmentForm
    template_name = "department/form.html"
    slug_field = "slug"
    slug_url_kwarg = "department_slug"

    def get_success_url(self):
        facility_slug = self.kwargs.get("facility_slug")
        return reverse(
            "facilities:departments:show",
            kwargs={
                "facility_slug": facility_slug,
                "department_slug": self.object.slug,
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        labels = self.request.session.get("organization_labels", {})
        context["title"] = labels.get("department_label", "Department")

        return context


class DeleteView(BaseDeleteView):
    """
    Delete-confirmation for a department.
    """

    model = Department
    template_name = "department/confirm_delete.html"
    success_url = reverse_lazy("departments:index")
