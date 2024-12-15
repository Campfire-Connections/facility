# facility/views/faculty.py

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin



from core.views.base import (
    BaseManageView,
    BaseTableListView,
    BaseCreateView,
    BaseDeleteView,
    BaseDetailView,
    BaseUpdateView,
    BaseFormView,
)
from user.models import User

from ..models.faculty import Faculty, FacultyProfile
from ..tables.faculty import FacultyTable
from ..forms.faculty import (
    FacultyForm,
    PromoteFacultyForm,
    AssignDepartmentForm,
    RegistrationForm,
)


class IndexView(BaseTableListView):
    model = User
    template_name = "faculty/index.html"
    context_object_name = "faculty"
    table_class = FacultyTable
    paginate_by = 10

    def get_queryset(self):
        return User.objects.filter(user_type=User.UserType.FACULTY)


class ManageView(BaseManageView):
    template_name = "faculty/manage.html"

    def test_func(self):
        return self.request.user.user_type == User.UserType.FACULTY and self.request.user.is_admin

    def get_tables_config(self):
        faculty_qs = User.objects.filter(
            facility=self.request.user.facultyprofile_profile.facility
        )
        return {
            "faculty": {
                "class": FacultyTable,
                "queryset": faculty_qs,
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


class CreateView(LoginRequiredMixin, BaseCreateView):
    model = FacultyProfile
    form_class = FacultyForm
    template_name = "faculty/form.html"
    success_url = reverse_lazy("facilities:faculty:index")
    action = "Create"
    success_message = "Faculty member created successfully!"
    error_message = "Failed to create faculty member."

class UpdateView(LoginRequiredMixin, BaseUpdateView):
    model = FacultyProfile
    form_class = FacultyForm
    template_name = "faculty/form.html"
    success_url = reverse_lazy("faculty:index")
    action = "Edit"


class PromoteView(LoginRequiredMixin, BaseUpdateView):
    model = FacultyProfile
    form_class = PromoteFacultyForm
    template_name = "faculty/promote.html"
    success_url = reverse_lazy("faculty:index")
    action = "Promote"


class DeleteView(LoginRequiredMixin, BaseDeleteView):
    model = FacultyProfile
    template_name = "faculty/confirm_delete.html"
    success_url = reverse_lazy("faculty_index")
    action = "Delete"


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
