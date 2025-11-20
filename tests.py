from core.tests import BaseDomainTestCase


class FacilityModelTests(BaseDomainTestCase):
    def test_facility_root_organization_matches_top_parent(self):
        self.assertEqual(
            self.facility.get_root_organization(),
            self.parent_org,
        )
