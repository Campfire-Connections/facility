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
    BaseDashboardView,
)
from user.models import User
from enrollment.tables.faculty_class import ClassScheduleTable
from enrollment.tables.faculty import FacultyEnrollmentByFacilityEnrollmentTable
from enrollment.models.faculty import FacultyEnrollment
from reports.models import GeneratedReport
from reports.tables import GeneratedReportTable
from course.models.facility_class import FacilityClass

from ..models.faculty import Faculty, FacultyProfile
from ..tables.faculty import FacultyTable, FacultyByFacilityTable
from ..forms.faculty import (
    FacultyForm,
    PromoteFacultyForm,
    AssignDepartmentForm,
    RegistrationForm,
)


class IndexView(BaseTableListView):
    model = User
    template_name = "faculty/list.html"
    context_object_name = "faculty"
    table_class = FacultyTable
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.filter(user_type=User.UserType.FACULTY)

        # Check if 'facility_slug' is present in the URL
        facility_slug = self.kwargs.get("facility_slug")
        if facility_slug:
            queryset = queryset.filter(
                facultyprofile_profile__facility__slug=facility_slug
            )

        return queryset


class ManageView(BaseManageView):
    template_name = "faculty/manage.html"

    def test_func(self):
        return (
            self.request.user.user_type == User.UserType.FACULTY
            and self.request.user.is_admin
        )

    def get_tables_config(self):
        faculty_qs = FacultyEnrollment.objects.select_related("faculty__user").filter(
            facility_enrollment__facility=self.request.user.facultyprofile_profile.facility
        )
        print(faculty_qs)
        return {
            "faculty": {
                "class": FacultyEnrollmentByFacilityEnrollmentTable,
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
    template_name = "faculty/register.html"
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


class DashboardView(BaseDashboardView):
    """
    Dashboard for faculty members.
    """

    template_name = "faculty/dashboard.html"
    widgets = ["class_enrollments_widget", "resources_widget"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

    def get_widgets_config(self):
        """Define widgets for the faculty dashboard."""
        widgets = {
            "class_schedule": {
                "table_class": ClassScheduleTable,
                "queryset": self.get_class_schedule_queryset(),
                "priority": 1,
                "title": "Class Schedule",
            },
        }

        # Additional widgets for faculty admins
        if self.request.user.is_admin:
            widgets.update(
                {
                    "faculty_management": {
                        "table_class": FacultyEnrollmentByFacilityEnrollmentTable,  # Define separately
                        "queryset": self.get_faculty_management_queryset(),
                        "priority": 5,
                        "title": "Manage Faculty",
                    },
                    "reports_table": {
                        "table_class": GeneratedReportTable,
                        "queryset": self.get_reports_queryset(),
                        "title": "Reports",
                        "priority": 1,
                    },
                }
            )

        return widgets

    def get_class_schedule_queryset(self, facility_enrollment=None):
        """Fetch data for class schedule widget."""
        profile = self.request.user.facultyprofile_profile

        if not facility_enrollment:
            facility_enrollment = self.get_default_facility_enrollment(profile)

        if not facility_enrollment:
            return FacilityClass.objects.none()

        return FacultyEnrollment.objects.classes_for_faculty(
            faculty_profile=profile,
            facility_enrollment=facility_enrollment,
        )

    def get_default_facility_enrollment(self, profile):
        """
        Fetch the default facility enrollment for a faculty profile.
        Returns None if no enrollment is found.
        """
        first_enrollment = profile.enrollments.first()
        return first_enrollment.facility_enrollment if first_enrollment else None

    def get_faculty_management_queryset(self):
        """Fetch data for faculty management widget (admin only)."""
        return self.request.user.facultyprofile_profile.facility.faculty.all()

    def get_reports_queryset(self):
        user = self.request.user

        # Reports created by the user
        created_reports = GeneratedReport.objects.filter(generated_by=user)

        # Reports associated with the user type
        user_reports = GeneratedReport.objects.filter(template__available_to=user)

        # Combine the QuerySets
        reports_queryset = created_reports | user_reports

        return reports_queryset.distinct()
