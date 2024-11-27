# facility/forms/quarters.py

from django import forms

from ..models.quarters import Quarters, QuartersType


class QuartersForm(forms.ModelForm):
    class Meta:
        model = Quarters
        fields = [
            "name",
            "description",
            "facility",
            "type",
        ]


class QuartersTypeForm(forms.ModelForm):
    class Meta:
        model = QuartersType
        fields = ["name", "description", "organization"]
