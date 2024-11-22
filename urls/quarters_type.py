# facility/urls/quarters_type.py

from django.urls import path
from ..views.quarters import (
    QuartersTypeIndexView,
    QuartersTypeShowView,
    QuartersTypeCreateView,
    QuartersTypeUpdateView,
    QuartersTypeDeleteView,
    QuartersTypeIndexByOrganizationView,
)

app_name = "types"

urlpatterns = [
    # Index
    path("", QuartersTypeIndexView.as_view(), name="index"),
    # Show
    path("<slug:slug>/", QuartersTypeShowView.as_view(), name="show"),
    path("<int:pk>/", QuartersTypeShowView.as_view(), name="show"),
    # Create
    path("new/", QuartersTypeCreateView.as_view(), name="new"),
    # Update
    path("<slug:slug>/update/", QuartersTypeUpdateView.as_view(), name="update"),
    path("<int:pk>/update/", QuartersTypeUpdateView.as_view(), name="update"),
    # Delete
    path("<slug:slug>/delete/", QuartersTypeDeleteView.as_view(), name="delete"),
    path("<int:pk>/delete/", QuartersTypeDeleteView.as_view(), name="delete"),
    # By Organization
    path(
        "organizations/<slug:organization_slug>/quarters/types/",
        QuartersTypeIndexByOrganizationView.as_view(),
        name="index_by_organization",
    ),
    path(
        "organizations/<int:organization_pk>/quarters/types/",
        QuartersTypeIndexByOrganizationView.as_view(),
        name="index_by_organization",
    ),
]
