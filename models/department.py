""" Department Related Models. """

from django.db import models
from django.urls import reverse

from pages.mixins import models as mixins
from pages.mixins import settings as stgs


class Department(
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
    """
    Department represents a department within a facility, encapsulating its attributes and 
    behaviors.

    This model inherits from various mixins to provide additional functionalities such as name and 
    description handling, timestamps, soft deletion, auditing, slug management, active status, 
    image handling, and parent-child relationships. It includes fields for the department's 
    abbreviation and a foreign key relationship to the associated facility, allowing for structured 
    organization within the facility.

    Attributes:
        abbreviation: A character field representing the department's abbreviation.
        facility: A foreign key linking the department to its associated facility.

    Methods:
        __str__():
            Returns a string representation of the department, typically its name.

        get_absolute_url():
            Constructs the absolute URL for a department instance, allowing for easy navigation to 
            its detail view.

        get_fallback_chain():
            Returns a predefined chain of related model names for fallback purposes.

    Returns:
        str: The absolute URL for the department's detail view from the get_absolute_url method.
        list: A list of strings representing the fallback chain of model names from the 
            get_fallback_chain method.
    """

    abbreviation = models.CharField(max_length=50)
    facility = models.ForeignKey(
        "Facility", on_delete=models.CASCADE, related_name="departments"
    )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        """
        get_absolute_url constructs the absolute URL for a department instance, allowing for easy 
        navigation to its detail view.

        This method utilizes Django's reverse function to generate a URL based on the department's 
        associated facility and its own slug. It ensures that the correct URL is returned for 
        accessing the department's detail page.

        Returns:
            str: The absolute URL for the department's detail view.
        """

        return reverse(
            "facilities:departments:show",
            kwargs={"facility_slug": self.facility.slug, "department_slug": self.slug},
        )

    def get_fallback_chain(self):
        return ["facility", "facility.organization"]
