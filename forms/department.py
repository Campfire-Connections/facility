# facility/forms/department.py

from django import forms

from ..models.department import Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            "name",
            "description",
            "facility",
            "parent",
        ]
