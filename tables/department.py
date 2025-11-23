# facility/tables/department.py
"""
DepartmentTable is a Django table that organizes and displays information about departments within 
a facility, including their abbreviations, associated facilities, and parent departments.

This table is built using django-tables2 and provides a structured view of the Department model. It 
includes columns for department abbreviation, facility name, and parent department name, 
facilitating easy integration with Django views and templates.

Attributes:
    abbreviation: A column that displays the abbreviation of the department.
    facility: A column that displays the name of the facility associated with the department.
    parent: A column that displays the name of the parent department.

    Meta:
        model: The model associated with this table, which is Department.
        fields: The fields to be included in the table representation.

    url_namespace: The namespace for the URLs related to departments.
    urls: A dictionary defining URL patterns for adding, editing, and deleting departments.
"""

import django_tables2 as tables
from core.tables.base import BaseTable

from ..models.department import Department


class DepartmentTable(BaseTable):
    """
    CourseTable is a Django table that organizes and displays information about courses, including
    their names, descriptions, images, and active status.

    This table is built using django-tables2 and provides a structured view of the Course model. It
    includes columns for course name, description, image representation, and the active status of
    the course. The `render_active` method formats the active status into a visually distinct
    badge, indicating whether the course is active or inactive.

    Attributes:
        name: A column that displays the name of the course.
        description: A column that displays a brief description of the course.
        image: A column that displays an image associated with the course.
        active: A column that indicates whether the course is currently active.

        Meta:
            model: The model associated with this table, which is Course.
            fields: The fields to be included in the table representation.

    Methods:
        render_active(value):
            Formats the active status into a badge with appropriate styling.

    Args:
        value: A boolean indicating the active status of the course.

    Returns:
        A safe HTML string representing the active status as a badge.
    """

    abbreviation = tables.Column(verbose_name="Abbreviation")
    facility = tables.Column(accessor="facility__name", verbose_name="Facility")
    parent = tables.Column(accessor="parent__name", verbose_name="Parent")

    class Meta:
        model = Department
        fields = ("name", "parent", "facility", "abbreviation")
        order_by = "name"
        #template_name = "base/paginate.html"

    url_namespace = "facilities:departments"
    urls = {
        "add": {"kwargs": {"facility_slug": "facility_slug"}},
        "show": {
            "kwargs": {"facility_slug": "facility__slug", "department_slug": "slug"}
        },
        "edit": {
            "kwargs": {"facility_slug": "facility__slug", "department_slug": "slug"}
        },
        "delete": {
            "kwargs": {"facility_slug": "facility__slug", "department_slug": "slug"}
        },
    }
    available_actions = ["show", "edit", "delete"]
