# facility/tables/quarters.py

import django_tables2 as tables
from pages.tables.base import BaseTable

from ..models.quarters import Quarters


class QuartersTable(BaseTable):
    """
    QuartersTable is a Django table that organizes and displays information about quarters, 
    including their associated facility, type, capacity, and occupancy.

    This table is built using django-tables2 and provides a structured view of the Quarters model. 
    It includes columns for the facility name, type of quarters, capacity, and current occupancy, 
    facilitating easy integration with Django views and templates.

    Attributes:
        facility: A column that displays the name of the associated facility.
        type: A column that displays the type of quarters.
        capacity: A column that indicates the maximum capacity of the quarters.
        occupancy: A column that shows the current occupancy of the quarters.

        Meta:
            model: The model associated with this table, which is Quarters.
            fields: The fields to be included in the table representation.

        url_namespace: The namespace for the URLs related to quarters.
        urls: A dictionary defining URL patterns for adding, showing, editing, and deleting 
            quarters.
    """

    facility = tables.Column(verbose_name="Facility")
    type = tables.Column(verbose_name="Type")
    capacity = tables.Column(verbose_name="Capacity")
    occupancy = tables.Column(verbose_name="Occupancy")

    class Meta:
        model = Quarters
        fields = (
            "name",
            "description",
            "facility",
            "type",
            "capacity",
            "occupancy",
        )  # Adjust fields as necessary

    url_namespace = "facilities:quarters"
    urls = {
        "add": {"kwargs": {"facility_slug": "facility__slug"}},
        "show": {
            "kwargs": {"facility_slug": "facility__slug", "quarters_slug": "slug"}
        },
        "edit": {
            "kwargs": {"facility_slug": "facility__slug", "quarters_slug": "slug"}
        },
        "delete": {
            "kwargs": {"facility_slug": "facility__slug", "quarters_slug": "slug"}
        },
    }
