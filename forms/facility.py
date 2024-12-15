# facility/forms/facility.py

from django import forms

from core.forms.base import BaseForm
from core.mixins.forms import SuccessMessageMixin, PrefillFormMixin
from ..models.facility import Facility


class FacilityForm(SuccessMessageMixin, PrefillFormMixin, BaseForm):
    success_message = "Facility successfully saved."

    class Meta:
        model = Facility
        fields = [
            "name",
            "description",
            "address",
            "organization",
            "is_active",
            "image",
        ]

    def get_initial(self):
        """
        Prefill the organization field with the user's organization if available.
        """
        initial = super().get_initial()
        if self.user.is_authenticated and hasattr(self.user, "organization"):
            initial["organization"] = self.user.organization
        return initial

    def clean_name(self):
        """
        Ensure the facility name is unique within an organization.
        """
        name = self.cleaned_data.get("name")
        organization = self.cleaned_data.get("organization")
        if Facility.objects.filter(name=name, organization=organization).exists():
            raise forms.ValidationError(
                "A facility with this name already exists in the organization."
            )
        return name
