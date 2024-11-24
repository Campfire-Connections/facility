""" Quarters Related Models. """

from django.db import models
from django.urls import reverse

from core.mixins import models as mixins
# from core.mixins import settings as stgs

class QuartersType(mixins.NameDescriptionMixin, mixins.TimestampMixin, mixins.SoftDeleteMixin, mixins.AuditMixin, mixins.SlugMixin, mixins.ActiveMixin, mixins.ImageMixin, mixins.ParentChildMixin, models.Model): # , stgs.SettingsMixin):
    organization = models.ForeignKey(
        "organization.Organization", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name}"

    def get_fallback_chain(self):
        return ['organization']

class Quarters(mixins.NameDescriptionMixin, mixins.TimestampMixin, mixins.SoftDeleteMixin, mixins.AuditMixin, mixins.SlugMixin, mixins.ActiveMixin, mixins.ImageMixin, mixins.ParentChildMixin, models.Model): # , stgs.SettingsMixin):
    """Quarters Model."""

    capacity = models.IntegerField()
    type = models.ForeignKey(
        "QuartersType", on_delete=models.CASCADE, related_name="quarters"
    )
    facility = models.ForeignKey(
        "Facility", on_delete=models.CASCADE, related_name="quarters"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("quarters_show", kwargs={"quarters_slug": self.slug})

    def get_fallback_chain(self):
        return ['type', 'type.organization', 'facility', 'facility.organization']