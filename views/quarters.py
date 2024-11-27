# facility/views/quarters.py

from django.urls import reverse_lazy, reverse

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
    template_name = "quarters/index.html"
    table_class = QuartersTable
    context_object_name = "quarters"


class IndexByFacilityView(BaseIndexByFilterTableView):
    model = Quarters
    template_name = "quarters/index.html"
    context_object_name = "quarters"
    table_class = QuartersTable
    lookup_keys = ["facility_slug", "facility_pk"]
    filter_field = "facility"
    filter_model = Facility
    context_object_name_for_filter = "facility"


class IndexByQuartersTypeView(BaseIndexByFilterTableView):
    model = Quarters
    template_name = "quarters/index.html"
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
    template_name = "quarters/type/index.html"
    table_class = QuartersTypeTable
    context_object_name = "quarters types"


class QuartersTypeIndexByOrganizationView(BaseIndexByFilterTableView):
    model = QuartersType
    template_name = "quarters/type/index.html"
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
