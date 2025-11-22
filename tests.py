from types import SimpleNamespace
from unittest.mock import patch
from datetime import time

from django.test import RequestFactory
from django.http import Http404

from core.tests import BaseDomainTestCase, mute_profile_signals
from user.models import User
from .models.faculty import FacultyProfile
from .models.quarters import Quarters, QuartersType
from .forms.quarters import QuartersForm
from .views.faculty import ManageView
from facility.models.department import Department
from enrollment.models.faculty import FacultyEnrollment as FacultyEnrollmentRecord
from enrollment.models.facility_class import (
    FacilityClassEnrollment as FacilityClassSchedule,
)
from enrollment.models.faculty_class import FacultyClassEnrollment as FacultyClassAssignment  # noqa: F401
from enrollment.models.temporal import Week, Period
from course.models.facility_class import FacilityClass
from enrollment.views.facility import (
    FacultyClassEnrollmentCreateView,
    FacultyClassEnrollmentUpdateView,
)
from enrollment.models.faculty import FacultyEnrollment as FacultyEnrollmentRecord
from enrollment.views.facility import (
    FacultyEnrollmentCreateView,
    FacultyEnrollmentUpdateView,
)


class FacilityModelTests(BaseDomainTestCase):
    def test_facility_root_organization_matches_top_parent(self):
        self.assertEqual(
            self.facility.get_root_organization(),
            self.parent_org,
        )


class FacultyManageViewTests(BaseDomainTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        with mute_profile_signals():
            self.user = User.objects.create_user(
                username="faculty.admin",
                password="pass12345",
                user_type=User.UserType.FACULTY,
                is_admin=True,
            )
        FacultyProfile.objects.create(
            user=self.user,
            organization=self.organization,
            facility=self.facility,
        )

    def test_get_facility_from_profile(self):
        request = self.factory.get("/facilities/manage/")
        request.user = self.user
        view = ManageView()
        view.request = request
        facility = view.get_facility()
        self.assertEqual(facility, self.facility)

    def test_get_facility_missing_profile_raises(self):
        with mute_profile_signals():
            orphan_user = User.objects.create_user(
                username="orphan.faculty",
                password="pass12345",
                user_type=User.UserType.FACULTY,
                is_admin=True,
            )
        request = self.factory.get("/facilities/manage/")
        request.user = orphan_user
        view = ManageView()
        view.request = request
        with self.assertRaises(Http404):
            view.get_facility()


class QuartersFormTests(BaseDomainTestCase):
    def test_duplicate_name_within_facility_is_invalid(self):
        quarters_type = QuartersType.objects.create(
            name="QA Type",
            organization=self.organization,
        )
        Quarters.objects.create(
            name="Cabin Alpha",
            facility=self.facility,
            type=quarters_type,
            capacity=10,
        )
        form = QuartersForm(
            data={
                "name": "Cabin Alpha",
                "facility": self.facility.id,
                "type": quarters_type.id,
                "capacity": 8,
                "description": "",
            }
        )
        self.assertFalse(form.is_valid())


class FacultyEnrollmentViewTests(BaseDomainTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        with mute_profile_signals():
            self.user = User.objects.create_user(
                username="faculty.coordinator",
                password="pass12345",
                user_type=User.UserType.FACULTY,
                is_admin=True,
            )
        self.profile = FacultyProfile.objects.create(
            user=self.user,
            organization=self.organization,
            facility=self.facility,
        )
        self.quarters_type = QuartersType.objects.create(
            name="Faculty Cabin",
            organization=self.organization,
        )
        self.quarters = Quarters.objects.create(
            name="Cabin Delta",
            facility=self.facility,
            type=self.quarters_type,
            capacity=2,
        )

    def _build_form(self, role="Guide"):
        return SimpleNamespace(
            cleaned_data={
                "faculty": self.profile,
                "facility_enrollment": self.facility_enrollment,
                "quarters": self.quarters,
                "role": role,
            },
            instance=None,
            add_error=lambda *args, **kwargs: None,
        )

    def _build_request(self):
        request = self.factory.post("/facilities/faculty/enrollments/new/")
        request.user = self.user
        return request

    def test_create_view_invokes_scheduling_service(self):
        view = FacultyEnrollmentCreateView()
        view.request = self._build_request()
        view.kwargs = {
            "facility_slug": self.facility.slug,
            "faculty_slug": self.profile.slug,
        }
        view.get_success_url = lambda: "/next/"
        form = self._build_form()

        with patch.object(
            FacultyEnrollmentCreateView, "service_class"
        ) as service_cls:
            service_instance = service_cls.return_value
            service_instance.schedule_faculty_enrollment.return_value = SimpleNamespace(
                pk=1
            )
            response = view.form_valid(form)

        service_instance.schedule_faculty_enrollment.assert_called_once_with(
            faculty=self.profile,
            facility_enrollment=self.facility_enrollment,
            quarters=self.quarters,
            role="Guide",
        )
        self.assertEqual(response.status_code, 302)

    def test_update_view_passes_existing_instance(self):
        existing = FacultyEnrollmentRecord.objects.create(
            name="Existing",
            faculty=self.profile,
            facility_enrollment=self.facility_enrollment,
            quarters=self.quarters,
        )
        view = FacultyEnrollmentUpdateView()
        view.request = self._build_request()
        view.kwargs = {
            "facility_slug": self.facility.slug,
            "faculty_slug": self.profile.slug,
        }
        view.get_object = lambda: existing
        view.get_success_url = lambda: "/next/"
        form = self._build_form(role="Lead")

        with patch.object(
            FacultyEnrollmentUpdateView, "service_class"
        ) as service_cls:
            service_instance = service_cls.return_value
            service_instance.schedule_faculty_enrollment.return_value = (
                SimpleNamespace(pk=2)
            )
            response = view.form_valid(form)

        service_instance.schedule_faculty_enrollment.assert_called_once_with(
            faculty=self.profile,
            facility_enrollment=self.facility_enrollment,
            quarters=self.quarters,
            role="Lead",
            instance=existing,
        )
        self.assertEqual(response.status_code, 302)


class FacultyClassAssignmentViewTests(BaseDomainTestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        with mute_profile_signals():
            self.user = User.objects.create_user(
                username="faculty.coordinator2",
                password="pass12345",
                user_type=User.UserType.FACULTY,
                is_admin=True,
            )
        self.profile = FacultyProfile.objects.create(
            user=self.user,
            organization=self.organization,
            facility=self.facility,
        )
        self.quarters_type = QuartersType.objects.create(
            name="Faculty Cabin B",
            organization=self.organization,
        )
        self.quarters = Quarters.objects.create(
            name="Cabin Echo",
            facility=self.facility,
            type=self.quarters_type,
            capacity=2,
        )
        self.faculty_enrollment = FacultyEnrollmentRecord.objects.create(
            name="Summer Faculty",
            faculty=self.profile,
            facility_enrollment=self.facility_enrollment,
            quarters=self.quarters,
        )
        self.department = Department.objects.create(
            name="Program Dept",
            abbreviation="PRG",
            facility=self.facility,
        )
        self.week = Week.objects.create(
            name="Week A",
            start=self.facility_enrollment.start,
            end=self.facility_enrollment.end,
            facility_enrollment=self.facility_enrollment,
        )
        self.period = Period.objects.create(
            name="Morning",
            start=time(8, 0),
            end=time(9, 0),
            week=self.week,
        )
        self.facility_class = FacilityClass.objects.create(
            name="First Aid Skills",
            organization_course=self.org_course,
            facility_enrollment=self.facility_enrollment,
        )
        self.class_enrollment = FacilityClassSchedule.objects.create(
            facility_class=self.facility_class,
            period=self.period,
            department=self.department,
            organization_enrollment=self.org_enrollment,
            max_enrollment=20,
        )

    def _build_request(self):
        request = self.factory.post("/facilities/faculty/class-enrollments/new/")
        request.user = self.user
        return request

    def _build_form(self):
        return SimpleNamespace(
            cleaned_data={
                "faculty": self.profile,
                "facility_class_enrollment": self.class_enrollment,
                "faculty_enrollment": self.faculty_enrollment,
            },
            add_error=lambda *args, **kwargs: None,
        )

    def test_faculty_class_assignment_create_uses_service(self):
        view = FacultyClassEnrollmentCreateView()
        view.request = self._build_request()
        view.kwargs = {
            "facility_slug": self.facility.slug,
            "faculty_slug": self.profile.slug,
            "faculty_enrollment_slug": self.faculty_enrollment.slug,
        }
        view.get_success_url = lambda: "/next/"
        form = self._build_form()

        with patch.object(
            FacultyClassEnrollmentCreateView, "service_class"
        ) as service_cls:
            service_instance = service_cls.return_value
            service_instance.assign_faculty_to_class.return_value = SimpleNamespace(
                pk=10
            )
            response = view.form_valid(form)

        service_instance.assign_faculty_to_class.assert_called_once_with(
            faculty=self.profile,
            facility_class_enrollment=self.class_enrollment,
            faculty_enrollment=self.faculty_enrollment,
        )
        self.assertEqual(response.status_code, 302)

    def test_faculty_class_assignment_update_passes_instance(self):
        existing = SimpleNamespace(pk=99)
        view = FacultyClassEnrollmentUpdateView()
        view.request = self._build_request()
        view.kwargs = {
            "facility_slug": self.facility.slug,
            "faculty_slug": self.profile.slug,
            "faculty_enrollment_slug": self.faculty_enrollment.slug,
        }
        view.get_object = lambda: existing
        view.get_success_url = lambda: "/next/"
        form = self._build_form()

        with patch.object(
            FacultyClassEnrollmentUpdateView, "service_class"
        ) as service_cls:
            service_instance = service_cls.return_value
            service_instance.assign_faculty_to_class.return_value = SimpleNamespace(
                pk=11
            )
            response = view.form_valid(form)

        service_instance.assign_faculty_to_class.assert_called_once_with(
            faculty=self.profile,
            facility_class_enrollment=self.class_enrollment,
            faculty_enrollment=self.faculty_enrollment,
            assignment=existing,
        )
        self.assertEqual(response.status_code, 302)
