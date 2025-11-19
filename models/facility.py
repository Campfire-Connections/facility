# facility/models/facility.py

from django.db import models
from django.urls import reverse

from core.mixins import models as mixins
from core.mixins import settings as stgs


class Facility(mixins.HierarchicalEntity, mixins.AddressableMixin, stgs.SettingsMixin, models.Model):
    """Facility Model."""
    organization = models.ForeignKey(
        "organization.Organization", on_delete=models.CASCADE, related_name="facilities"
    )

    class Meta:
        verbose_name = "Facility"
        verbose_name_plural = "Facilities"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("facility_show", kwargs={"facility_slug": self.slug})

    def get_root_organization(self):
        return self.organization.get_root_organization()

    def get_fallback_chain(self):
        return ['organization']

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "slug"], name="unique_facility_slug_per_org"
            )
        ]
