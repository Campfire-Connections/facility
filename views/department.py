# facility/views/department.py

from django.views.generic import (
    ListView as _ListView,
    DetailView as _DetailView,
    CreateView as _CreateView,
    UpdateView as _UpdateView,
    DeleteView as _DeleteView,
    TemplateView,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django_tables2 import SingleTableMixin

from core.mixins.forms import SuccessMessageMixin, FormValidMixin
from core.mixins.models import SoftDeleteMixin

from ..models.department import Department
from ..models.facility import Facility
from ..tables.department import DepartmentTable


class IndexView(_ListView):
    model = Department
    template_name = "department/list.html"
    context_object_name = "departments"


class IndexByFacilityView(SingleTableMixin, TemplateView):
    model = Department
    table_class = DepartmentTable
    template_name = "department/list.html"
    context_object_name = "departments"

    def get_queryset(self):
        """Return departments associated with the selected facility."""
        self.facility = self.get_facility()
        return Department.objects.filter(facility=self.facility)

    def get_context_data(self, **kwargs):
        """Add facility to context for template usage."""
        context = super().get_context_data(**kwargs)
        context["facility"] = self.facility
        return context

    def get_facility(self):
        """Helper method to retrieve the facility by ID or slug."""
        facility_id = self.kwargs.get("facility_id")
        facility_slug = self.kwargs.get("facility_slug")

        if facility_id:
            return get_object_or_404(Facility, pk=facility_id)
        return get_object_or_404(Facility, slug=facility_slug)


class ShowView(_DetailView):
    model = Department
    template_name = "department/show.html"
    context_object_name = "department"

    def get_object(self):
        department_id = self.kwargs.get("department_id")
        department_slug = self.kwargs.get("department_slug")
        if department_id:
            return get_object_or_404(Department, pk=department_id)
        else:
            return get_object_or_404(Department, slug=department_slug)


class CreateView(LoginRequiredMixin, UserPassesTestMixin, _CreateView):
    model = Department
    template_name = "department/form.html"
    fields = ["name", "description", "abbreviation", "facility", "parent"]

    def test_func(self):
        return self.request.user.user_type == "FACULTY" and self.request.user.is_admin

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form submission.
        """
        facility_slug = self.kwargs.get('facility_slug')
        department_slug = self.object.slug  # Assuming the department has a slug field

        # Generate the URL dynamically with both slugs
        return reverse('facilities:departments:show', kwargs={
            'facility_slug': facility_slug,
            'department_slug': department_slug
        })


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, _UpdateView):
    model = Department
    context_object_name = "department"
    template_name = "department/form.html"
    fields = ["name", "description", "abbreviation", "parent", "facility"]
    success_url = reverse_lazy("facilities:departments:show")
    slug_url_kwarg = "department_slug"

    def test_func(self):
        return self.request.user.user_type == "FACULTY" and self.request.user.is_admin

    def get_queryset(self):
        facility_slug = self.kwargs.get("facility_slug")
        return Department.objects.filter(facility__slug=facility_slug)

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form submission.
        """
        facility_slug = self.kwargs.get("facility_slug")
        department_slug = self.object.slug  # Assuming the department has a slug field

        return reverse(
            "facilities:departments:show",
            kwargs={"facility_slug": facility_slug, "department_slug": department_slug},
        )


class DeleteView(LoginRequiredMixin, UserPassesTestMixin, _DeleteView):
    model = Department
    template_name = "department/confirm_delete.html"
    success_url = reverse_lazy("departments:index")

    def test_func(self):
        return self.request.user.user_type == "FACULTY" and self.request.user.is_admin
