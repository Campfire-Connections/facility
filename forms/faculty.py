# facility/forms/faculty.py
"""Faculty Related Forms."""

from django import forms

from course.models.facility_class import FacilityClass
from user.models import User
from user.forms import ProfileUserFieldsMixin, RegistrationForm

from ..models.faculty import FacultyProfile
from ..models.quarters import Quarters
from ..models.department import Department
from ..models.facility import Facility


class FacultyRegistrationForm(RegistrationForm):
    """A specialized registration form for faculty user creation.

    Extends the base RegistrationForm to include additional faculty-specific fields like first
    name, last name, and facility.

    Attributes:
        first_name: A required text input field for the faculty member's first name.
        last_name: A required text input field for the faculty member's last name.
        facility: A required model choice field for selecting the faculty's facility.

    Methods:
        save: Overrides the default save method to set the user type as faculty and create an
            associated FacultyProfile.
    """

    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "First Name"}
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Last Name"}
        ),
    )
    facility = forms.ModelChoiceField(
        queryset=Facility.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta(RegistrationForm.Meta):
        model = User
        fields = RegistrationForm.Meta.fields + ["first_name", "last_name"]

    def save(self, commit=True):
        """Saves a user with faculty-specific attributes and creates an associated faculty profile.

        Overrides the default save method to set the user type and optionally create a faculty
        profile. Ensures the user is marked as a faculty member in the system.

        Args:
            commit: A boolean flag to determine whether to save the user and create the faculty
                profile immediately.

        Returns:
            User: The created user instance with faculty type.
        """

        user = super().save(commit=False)
        user.user_type = User.UserType.FACULTY  # Set the user type as 'Faculty'
        if commit:
            user.save()
            # Create the FacultyProfile associated with this user
            FacultyProfile.objects.create(
                user=user, facility=self.cleaned_data["facility"]
            )
        return user


class FacultyForm(ProfileUserFieldsMixin):
    """A comprehensive form for creating a new faculty user with detailed information.

    Provides a form interface for registering a faculty member with personal details, email,
    password, and facility selection.

    Attributes:
        first_name: A required text input for the faculty member's first name.
        last_name: A required text input for the faculty member's last name.
        email: A required email field for the faculty member's contact information.
        password: A required password input field.
        confirm_password: A required password confirmation field.
        facility: A required model choice field for selecting the faculty's facility.

    Methods:
        clean: Validates that the password and confirmation password match.
        save: Creates both a User and FacultyProfile with the provided information.
    """

    facility = forms.ModelChoiceField(
        queryset=Facility.objects.all(),
        required=True,
    )

    class Meta:
        model = FacultyProfile
        fields = ["facility"]  # Fields specific to FacultyProfile

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.user.user_type = User.UserType.FACULTY
        if commit:
            profile.user.save()
            profile.save()
        return profile


class PromoteFacultyForm(forms.ModelForm):
    """A form for promoting a faculty member to an administrative role.

    Provides a simple interface to toggle a user's administrative status using a checkbox input.

    Attributes:
        is_admin: A checkbox field to set or unset administrative privileges for a user.
    """

    class Meta:
        model = User
        fields = ["is_admin"]
        widgets = {
            "is_admin": forms.CheckboxInput(attrs={"class": "form-control"}),
        }


class AssignDepartmentForm(forms.ModelForm):
    """
    Form for assigning a faculty member to a department.
    """

    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = FacultyProfile
        fields = ["department"]


class AssignClassForm(forms.ModelForm):
    """
    Form for assigning a faculty member to a class.
    """

    facility_class = forms.ModelChoiceField(
        queryset=FacilityClass.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = FacultyProfile
        fields = ["facility_class"]


class ChangeQuartersForm(forms.ModelForm):
    """
    Form for changing the quarters assigned to a faculty member.
    """

    quarters = forms.ModelChoiceField(
        queryset=Quarters.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = FacultyProfile
        fields = ["quarters"]
