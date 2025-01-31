# facility/forms/quarters.py

from django import forms

from core.forms.base import BaseForm
from core.mixins.forms import SuccessMessageMixin, FormValidationMixin

from ..models.quarters import Quarters, QuartersType


class QuartersForm(SuccessMessageMixin, BaseForm, FormValidationMixin):
    """A form for creating and managing quarters within a facility.

    Provides a comprehensive interface for defining quarters with unique naming constraints and
    facility-specific details.

    Attributes:
        success_message: A message displayed upon successful quarters creation or update.

    Methods:
        clean_name: Validates that the quarters name is unique within a specific facility.
    """

    success_message = "Quarters successfully saved."

    class Meta:
        model = Quarters
        fields = [
            "name",
            "description",
            "facility",
            "type",
            "capacity"
        ]

    def clean_name(self):
        """
        Ensure that Quarters name is unique within a facility.
        """
        name = self.cleaned_data.get("name")
        facility = self.cleaned_data.get("facility")
        if Quarters.objects.filter(name=name, facility=facility).exists():
            raise forms.ValidationError(
                "Quarters with this name already exist in the facility."
            )
        return name


class QuartersTypeForm(SuccessMessageMixin, BaseForm):
    """A form for creating and managing quarters type within an organization.

    Provides an interface for defining unique quarters types with organizational context and
    descriptive details.

    Attributes:
        success_message: A message displayed upon successful quarters type creation or update.

    Methods:
        clean_name: Validates that the quarters type name is unique within a specific organization.
    """

    success_message = "Quarters type successfully saved."

    class Meta:
        model = QuartersType
        fields = ["name", "description", "organization"]

    def clean_name(self):
        """
        Ensure that QuartersType name is unique within an organization.
        """
        name = self.cleaned_data.get("name")
        organization = self.cleaned_data.get("organization")
        if QuartersType.objects.filter(name=name, organization=organization).exists():
            raise forms.ValidationError(
                "A quarters type with this name already exists in the organization."
            )
        return name
