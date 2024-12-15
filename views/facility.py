# facility/views/facility.py

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404

from organization.models.organization import Organization
from enrollment.models.facility import FacilityEnrollment
from enrollment.tables.facility import FacilityEnrollmentTable
from course.models.facility_class import FacilityClass
from course.tables.facility_class import FacilityClassTable
from user.models import User
from core.views.base import (
    BaseManageView,
    BaseIndexByFilterTableView,
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseTableListView,
    BaseUpdateView,
)

from ..models.facility import Facility
from ..forms.facility import FacilityForm
from ..tables.facility import FacilityTable
from ..models.department import Department
from ..tables.department import DepartmentTable
from ..models.quarters import Quarters
from ..tables.quarters import QuartersTable
from ..tables.faculty import FacultyTable


class IndexView(BaseTableListView):
    model = Facility
    template_name = "facility/index.html"
    table_class = FacilityTable
    context_object_name = "facilities"


class IndexByOrganizationView(BaseIndexByFilterTableView):
    model = Facility
    template_name = "facility/index.html"
    context_object_name = "facilities"
    table_class = FacilityTable
    lookup_keys = ["organization_slug", "organization_pk"]
    filter_field = "organization"
    filter_model = Organization
    context_object_name_for_filter = "organization"


class ManageView(BaseManageView):
    template_name = "facility/manage.html"

    def get_facility(self):
        """
        Get the facility associated with the current user.
        """
        user = self.request.user
        for f in user._meta.get_fields():
            if hasattr(user, f.name):
                print(f"{f.name}: {getattr(user, f.name)}")
        profile = user.get_profile()
        print(profile)
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

    def test_func(self):
        """
        Check if the user is a faculty member with admin privileges.
        """
        return self.request.user.user_type == "FACULTY" and self.request.user.is_admin

    def get_create_url(self, table):
        facility = self.get_facility()
        return table.get_url("add", context={"facility_slug": facility.slug})


class ShowView(BaseDetailView):
    """
    View class for displaying detailed information about a specific facility. This class extends
    BaseDetailView to provide a structured way to present various tables related to the facility,
    including departments, quarters, faculty, and enrollments.

    Attributes:
        model (type): The model class associated with the view, in this case, Facility.
        template_name (str): The name of the template used to render the view.
        context_object_name (str): The name of the context variable for the facility object.
        slug_field (str): The field used to identify the facility in the URL.
        slug_url_kwarg (str): The URL keyword argument that contains the facility slug.

    Methods:
        get_tables_config(): Returns a configuration dictionary for the tables associated with the
        facility, including their classes and querysets.

    Args:
        self: The instance of the class.

    Returns:
        dict: A dictionary containing the configuration for the tables related to the facility.
    """

    model = Facility
    template_name = "facility/show.html"
    context_object_name = "facility"
    slug_field = "slug"
    slug_url_kwarg = "facility_slug"

    def get_tables_config(self):
        """
        View class for displaying detailed information about a specific facility. This class
        extends BaseDetailView to provide a structured way to present various tables related to the
        facility, including departments, quarters, faculty, and enrollments.

        Attributes:
            model (type): The model class associated with the view, in this case, Facility.
            template_name (str): The name of the template used to render the view.
            context_object_name (str): The name of the context variable for the facility object.
            slug_field (str): The field used to identify the facility in the URL.
            slug_url_kwarg (str): The URL keyword argument that contains the facility slug.

        Methods:
            get_tables_config(): Returns a configuration dictionary for the tables associated with
            the facility, including their classes and querysets.

        Args:
            self: The instance of the class.

        Returns:
            dict: A dictionary containing the configuration for the tables related to the facility.
        """

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
                "queryset": User.objects.filter(
                    user_type="FACULTY", facultyprofile__facility=facility
                ).select_related("facultyprofile"),
            },
            "facility_enrollment_table": {
                "class": FacilityEnrollmentTable,
                "queryset": FacilityEnrollment.objects.filter(facility=facility),
            },
        }


class CreateView(BaseCreateView):
    """
    View class for creating new instances of the Facility model. This class extends BaseCreateView
    to provide a form for creating facilities, specifying the model, form class, template, and
    success URL for redirection after a successful creation.

    Attributes:
        model (type): The model class associated with the view, in this case, Facility.
        form_class (type): The form class used for creating new instances of the model.
        template_name (str): The name of the template used to render the form.
        success_url (str): The URL to redirect to upon successful creation of a facility.

    Args:
        self: The instance of the class.
    """

    model = Facility
    form_class = FacilityForm
    template_name = "facility/form.html"
    success_url = reverse_lazy("facilities:index")


class UpdateView(BaseUpdateView):
    """
    View class for updating existing instances of the Facility model. This class extends
    BaseUpdateView to provide a form for editing facilities, specifying the model, form class, and
    template used for rendering the update form.

    Attributes:
        model (type): The model class associated with the view, in this case, Facility.
        form_class (type): The form class used for updating instances of the model.
        template_name (str): The name of the template used to render the form.

    Args:
        self: The instance of the class.
    """

    model = Facility
    form_class = FacilityForm
    template_name = "facility/form.html"
    success_url = reverse_lazy("facilities:index")


class DeleteView(BaseDeleteView):
    """
    View class for confirming the deletion of an existing instance of the Facility model. This
    class extends BaseDeleteView to provide a confirmation interface for deleting facilities,
    specifying the model and template used for rendering the confirmation page.

    Attributes:
        model (type): The model class associated with the view, in this case, Facility.
        template_name (str): The name of the template used to render the confirmation page.

    Args:
        self: The instance of the class.
    """

    model = Facility
    template_name = "facility/confirm_delete.html"
    success_url = reverse_lazy("facilities:index")
