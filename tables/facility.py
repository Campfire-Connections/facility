# facility/tables/facility.py
import django_tables2 as tables
from ..models.facility import Facility


class FacilityTable(tables.Table):
    class Meta:
        model = Facility
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", "address", "capacity")
        attrs = {"class": "table table-striped table-bordered"}
