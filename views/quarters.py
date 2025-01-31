# facility/views/quarters.py

from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django import forms

from organization.models.organization import Organization
from core.views.base import (
    BaseIndexByFilterTableView,
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseTableListView,
    BaseUpdateView,
)

from ..models.quarters import Quarters, QuartersType
from ..tables.quarters import QuartersTable, QuartersTypeTable
from ..forms.quarters import QuartersForm, QuartersTypeForm
from ..models.facility import Facility


class IndexView(BaseTableListView):
    model = Quarters
    template_name = "quarters/list.html"
    table_class = QuartersTable
    context_object_name = "quarters"


class IndexByFacilityView(BaseIndexByFilterTableView):
    model = Quarters
    template_name = "quarters/list.html"
    context_object_name = "quarters"
    table_class = QuartersTable
    lookup_keys = ["facility_slug", "facility_pk"]
    filter_field = "facility"
    filter_model = Facility
    context_object_name_for_filter = "facility"


class IndexByQuartersTypeView(BaseIndexByFilterTableView):
    model = Quarters
    template_name = "quarters/list.html"
    context_object_name = "quarters"
    table_class = QuartersTable
    filter_field = "type"
    filter_model = QuartersType
    context_object_name_for_filter = "quarters type"
    url_kwarg = "slug"


class ShowView(BaseDetailView):
    model = Quarters
    template_name = "quarters/show.html"
    context_object_name = "quarters"
    slug_field = "slug"
    slug_url_kwarg = "quarters_slug"

    def get_object(self):
        quarters_id = self.kwargs.get("quarters_id")
        quarters_slug = self.kwargs.get("quarters_slug")
        if quarters_id:
            return get_object_or_404(Quarters, pk=quarters_id)
        else:
            return get_object_or_404(Quarters, slug=quarters_slug)


class CreateView(BaseCreateView):
    model = Quarters
    form_class = QuartersForm
    template_name = "quarters/form.html"

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form submission.
        """
        facility_slug = self.kwargs.get("facility_slug")
        quarters_slug = self.object.slug

        # Generate the URL dynamically with both slugs
        return reverse(
            "facilities:quarters:show",
            kwargs={"facility_slug": facility_slug, "quarters_slug": quarters_slug},
        )

    def get_context_data(self, **kwargs):
        """
        Add additional context to the template.
        """
        context = super().get_context_data(**kwargs)

        # Access organization labels using the context processor
        labels = self.request.session.get("organization_labels", {})

        # Add the title to the context
        context["title"] = labels.get("quarters_label", "Quarters")

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
    model = Quarters
    form_class = QuartersForm
    template_name = "quarters/form.html"
    fields = ["name", "description", "capacity", "type", "facility"]

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form submission.
        """
        facility_slug = self.kwargs.get("facility_slug")
        quarters_slug = self.object.slug

        return reverse(
            "facilities:quarters:show",
            kwargs={"facility_slug": facility_slug, "quarters_slug": quarters_slug},
        )


class DeleteView(BaseDeleteView):
    model = Quarters
    template_name = "quarters/confirm_delete.html"

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form submission.
        """
        facility_slug = self.kwargs.get("facility_slug")
        quarters_slug = self.object.slug

        return reverse(
            "facilities:quarters:index",
            kwargs={"facility_slug": facility_slug},
        )


class QuartersTypeIndexView(BaseTableListView):
    model = QuartersType
    template_name = "quarters/type/list.html"
    table_class = QuartersTypeTable
    context_object_name = "quarters types"


class QuartersTypeIndexByOrganizationView(BaseIndexByFilterTableView):
    model = QuartersType
    template_name = "quarters/type/list.html"
    context_obect_name = "quarters types"
    table_class = QuartersTypeTable
    lookup_keys = ["organization_slug", "organization_pk"]
    filter_field = "organization"
    filter_model = Organization
    context_object_name_for_filter = "organization"


class QuartersTypeShowView(BaseDetailView):
    model = QuartersType
    template_name = "quarters/type/show.html"
    context_object_name = "quarters type"
    slug_field = "slug"
    slug_url_kwarg = "quarters_type_slug"


class QuartersTypeCreateView(BaseCreateView):
    model = QuartersType
    template_name = "quarters/type/form.html"
    success_url = reverse_lazy("facility:quarters:types:index")

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form submission.
        """
        facility_slug = self.kwargs.get("facility_slug")
        quarters_slug = self.kwargs.get("quarters_slug")
        type_slug = self.object.slug

        # Generate the URL dynamically with both slugs
        return reverse(
            "facilities:quarters:tyoes:show",
            kwargs={
                "facility_slug": facility_slug,
                "quarters_slug": quarters_slug,
                "type_slug": type_slug,
            },
        )


class QuartersTypeUpdateView(BaseUpdateView):
    model = QuartersType
    template_name = "quarters/type/form.html"
    fields = ["name", "description", "organization"]
    form_class = QuartersTypeForm

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form submission.
        """
        facility_slug = self.kwargs.get("facility_slug")
        quarters_slug = self.kwargs.get("quarters_slug")
        type_slug = self.object.slug

        return reverse(
            "facilities:quarters:types:show",
            kwargs={
                "facility_slug": facility_slug,
                "quarters_slug": quarters_slug,
                "type_slug": type_slug,
            },
        )


class QuartersTypeDeleteView(BaseDeleteView):
    model = QuartersType
    template_name = "quarters/type/confirm_delete.html"

    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form submission.
        """
        facility_slug = self.kwargs.get("facility_slug")
        quarters_slug = self.kwargs.get("quarters_slug")

        return reverse(
            "facilities:quarters:types:index",
            kwargs={"facility_slug": facility_slug, "quarters_slug": quarters_slug},
        )
