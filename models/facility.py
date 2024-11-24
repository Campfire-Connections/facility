# facility/models/facility.py

from django.db import models
from django.urls import reverse
from address.models import AddressField

from core.mixins import models as mixins
from core.mixins import settings as stgs


class Facility(
    mixins.NameDescriptionMixin,
    mixins.TimestampMixin,
    mixins.SoftDeleteMixin,
    mixins.AuditMixin,
    mixins.SlugMixin,
    mixins.ActiveMixin,
    mixins.ImageMixin,
    mixins.ParentChildMixin,
    stgs.SettingsMixin,
    models.Model,
):
    """Facility Model."""

    # address = GenericRelation("address.Address", null=True, blank=True)
    # address = models.CharField(max_length=255, null=True, blank=True)
    address = AddressField(blank=True, null=True)
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


