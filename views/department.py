# facility/views/department.py

from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from core.views.base import (
    BaseIndexByFilterTableView,
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseTableListView,
    BaseUpdateView,
)

from ..models.facility import Facility
from ..models.department import Department
from ..forms.department import DepartmentForm
from ..tables.department import DepartmentTable


class IndexView(BaseTableListView):
    model = Department
    template_name = "department/list.html"
    table_class = DepartmentTable
    context_object_name = "departments"


class IndexByFacilityView(BaseIndexByFilterTableView):
    model = Department
    template_name = "department/list.html"
    context_object_name = "departments"
    table_class = DepartmentTable
    lookup_keys = ["facility_slug", "facility_pk"]
    filter_field = "facility"
    filter_model = Facility
    context_object_name_for_filter = "facility"

class ShowView(BaseDetailView):
    model = Department
    template_name = "department/show.html"
    context_object_name = "department"
    slug_field = "slug"
    slug_url_kwarg = "department_slug"

    def get_object(self):
        department_id = self.kwargs.get("department_id")
        department_slug = self.kwargs.get("department_slug")
        if department_id:
            return get_object_or_404(Department, pk=department_id)
        else:
            return get_object_or_404(Department, slug=department_slug)


class CreateView(BaseCreateView):
    model = Department
    form_class = DepartmentForm
    template_name = "department/form.html"
    
    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form submission.
        """
        facility_slug = self.kwargs.get('facility_slug')
        department_slug = self.object.slug

        # Generate the URL dynamically with both slugs
        return reverse('facilities:departments:show', kwargs={
            'facility_slug': facility_slug,
            'department_slug': department_slug
        })


class UpdateView(BaseUpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = "department/form.html"
    fields = ["name", "description", "abbreviation", "parent", "facility"]

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form submission.
        """
        facility_slug = self.kwargs.get("facility_slug")
        department_slug = self.object.slug

        return reverse(
            "facilities:departments:show",
            kwargs={"facility_slug": facility_slug, "department_slug": department_slug},
        )


class DeleteView(BaseDeleteView):
    model = Department
    template_name = "department/confirm_delete.html"
    success_url = reverse_lazy("departments:index")
