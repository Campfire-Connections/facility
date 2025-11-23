# facility/urls/quarters.py

from django.urls import path, include

from ..views.quarters import (
    IndexView,
    IndexByFacilityView,
    IndexByQuartersTypeView,
    ShowView,
    CreateView,
    UpdateView,
    DeleteView,
)

app_name = "quarters"

urlpatterns = [
    # Quarters Types
    path("types/", include('facility.urls.quarters_type', namespace="types")),
    # Index
    path("", IndexView.as_view(), name="index"),
    path("facility/<slug:facility_slug>/", IndexByFacilityView.as_view(), name="index_by_facility"),
    # Show
    path("<int:pk>", ShowView.as_view(), name="show"),
    path("<slug:quarters_slug>", ShowView.as_view(), name="show"),
    # Create
    path("new/", CreateView.as_view(), name="new"),
    # Update
    path("<int:pk>/update/", UpdateView.as_view(), name="update"),
    path("<slug:quarters_slug>/update/", UpdateView.as_view(), name="update"),
    # Delete
    path("<int:pk>/delete/", DeleteView.as_view(), name="delete"),


]
