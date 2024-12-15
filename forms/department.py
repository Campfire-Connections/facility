# facility/forms/department.py

from django import forms

from core.forms.base import BaseForm
from core.mixins.forms import DynamicFieldMixin, SuccessMessageMixin

from ..models.department import Department


class DepartmentForm(SuccessMessageMixin, DynamicFieldMixin, BaseForm):
    """A form for creating and editing department information with dynamic field capabilities.

    Provides a comprehensive interface for managing department details with custom validation
    and field modification based on user permissions.

    Attributes:
        success_message: A message displayed upon successful department creation or update.

    Methods:
        clean_name: Validates the department name length.
        modify_form_fields: Dynamically adjusts form fields based on user role.
    """

    success_message = "Department successfully saved."

    class Meta:
        model = Department
        fields = [
            "name",
            "description",
            "facility",
            "parent",
        ]

    def clean_name(self):
        """Validates the length of the department name.

        Ensures that the department name does not exceed 50 characters in length.

        Returns:
            str: The validated department name.

        Raises:
            ValidationError: If the department name is longer than 50 characters.
        """

        name = self.cleaned_data.get("name")
        if len(name) > 50:
            raise forms.ValidationError("Department name cannot exceed 50 characters.")
        return name

    def modify_form_fields(self, form):
        """Dynamically modifies form fields based on user permissions.

        Removes the parent field from the form for non-staff users, restricting access to certain
        form elements.

        Args:
            form: The form instance to be modified.
        """

        if not self.user.is_staff:
            form.fields.pop("parent", None)
