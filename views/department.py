# facility/views/department.py

from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django import forms

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
        facility_slug = self.kwargs.get("facility_slug")
        department_slug = self.object.slug

        # Generate the URL dynamically with both slugs
        return reverse(
            "facilities:departments:show",
            kwargs={"facility_slug": facility_slug, "department_slug": department_slug},
        )

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template.
        """
        context = super().get_context_data(**kwargs)

        # Access organization labels using the context processor
        labels = self.request.session.get("organization_labels", {})

        # Add the title to the context
        context["title"] = labels.get("department_label", "Department")

        return context

    def get_initial(self):
        """
        Prepopulate form fields with initial values.
        """
        initial = super().get_initial()
        facility_slug = self.kwargs.get("facility_slug")

        # Fetch the Facility object based on the slug
        try:
            facility = Facility.objects.get(slug=facility_slug)
            initial["facility"] = facility  # Prepopulate the 'facility' field
        except Facility.DoesNotExist:
            pass

        return initial

    def get_form(self, *args, **kwargs):
        """
        Optionally customize the form to make the 'facility' field hidden.
        """
        form = super().get_form(*args, **kwargs)
        facility_slug = self.kwargs.get("facility_slug")

        # Set the facility field as hidden and prepopulate its value
        if facility_slug:
            try:
                facility = Facility.objects.get(slug=facility_slug)
                form.fields["facility"].initial = facility
                form.fields["facility"].widget = forms.HiddenInput()
                form.fields["facility"].label = None
            except Facility.DoesNotExist:
                pass

        return form

    def form_valid(self, form):
        # Check if the request is an AJAX request
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            response_data = {"success": True, "redirect_url": self.get_success_url()}
            return JsonResponse(response_data)

        # Default behavior for non-AJAX requests
        return super().form_valid(form)


class UpdateView(BaseUpdateView):
    model = Department
    form_class = DepartmentForm
    template_name = "department/form.html"
    #fields = ["name", "description", "abbreviation", "parent", "facility"]
    slug_field = "slug"  # The field in the model
    slug_url_kwarg = "department_slug"
    
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

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template.
        """
        context = super().get_context_data(**kwargs)

        # Access organization labels using the context processor
        labels = self.request.session.get("organization_labels", {})

        # Add the title to the context
        context["title"] = labels.get("department_label", "Department")

        return context


class DeleteView(BaseDeleteView):
    model = Department
    template_name = "department/confirm_delete.html"
    success_url = reverse_lazy("departments:index")
