# facility/views/faculty.py

from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404

from core.views.base import (
    BaseManageView,
    BaseIndexByFilterTableView,
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseTableListView,
    BaseUpdateView,
    BaseFormView,
)

from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelformset_factory
from django.contrib import messages
from django_tables2 import MultiTableMixin, SingleTableView

from user.models import User
from user.mixins import AdminRequiredMixin
from organization.models.organization import Organization

from ..models.facility import Facility
from ..models.faculty import Faculty, FacultyProfile
from ..tables.faculty import FacultyTable
from ..forms.faculty import (
    RegistrationForm,
    FacultyForm,
    PromoteFacultyForm,
    AssignDepartmentForm,
    AssignClassForm,
    ChangeQuartersForm,
)


class IndexView(BaseTableListView):
    model = User
    template_name = "faculty/index.html"
    context_object_name = "faculty"
    table_class = FacultyTable

    def get_queryset(self):
        return User.objects.filter(role="FACULTY")


class ManageView(BaseManageView):
    template_name = "faculty/manage.html"

    def test_func(self):
        return self.request.user.user_type == "FACULTY" and self.request.user.is_admin

    def get_tables_config(self):
        return {
            "faculty": {
                "class": FacultyTable,
                "queryset": Faculty.objects.filter(
                    facility=self.request.user.facultyprofile.facility
                ),
            }
        }

    def get_forms_config(self):
        return {
            "faculty_form": FacultyForm,
            "promotion_form": PromoteFacultyForm,
            "department_form": AssignDepartmentForm,
            "class_form": ClassAssignmentForm,
            "quarters_form": QuartersAssignmentForm,
        }


class CreateView(BaseCreateView):
    model = FacultyProfile
    form_class = FacultyForm
    template_name = "faculty/form.html"
    success_url = reverse_lazy("facilities:faculty:index")
    action = "Create"


class UpdateView(BaseUpdateView):
    model = FacultyProfile
    form_class = FacultyForm
    template_name = "faculty/form.html"
    success_url = reverse_lazy("faculty:index")
    action = "Edit"


class PromoteView(BaseUpdateView):
    model = FacultyProfile
    form_class = PromoteFacultyForm
    template_name = "faculty/promote.html"
    success_url = reverse_lazy("faculty:index")
    action = "Promote"


class IndexByFacilityView(BaseIndexByFilterTableView):
    model = Faculty
    table_class = FacultyTable
    template_name = "faculty/index.html"
    filter_field = "facultyprofile__facility"
    related_model = Facility
    url_kwarg = "facility_slug"


class DeleteView(BaseDeleteView):
    model = FacultyProfile
    template_name = "faculty/confirm_delete.html"
    success_url = reverse_lazy("faculty_index")
    action = "Delete"


class IndexByOrganizationView(BaseIndexByFilterTableView):
    model = Faculty
    table_class = FacultyTable
    template_name = "faculty/index.html"
    filter_field = "organization"
    related_model = Organization
    url_kwarg = "organization_slug"


class ShowView(BaseDetailView):
    model = Faculty
    template_name = "faculty/show.html"
    context_object_name = "faculty"


class RegisterFacultyView(BaseFormView):
    template_name = "register_faculty.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        raw_password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=raw_password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
