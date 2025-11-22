from django.test import RequestFactory
from django.http import Http404

from core.tests import BaseDomainTestCase, mute_profile_signals
from user.models import User
from .models.faculty import FacultyProfile
from .models.quarters import Quarters, QuartersType
from .forms.quarters import QuartersForm
from .views.faculty import ManageView


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
