# facility/urls/facility.py

from django.urls import path, include

from ..views.facility import (
    IndexView,
    ShowView,
    CreateView,
    UpdateView,
    DeleteView,
    ManageView,
)

app_name = "facilities"

urlpatterns = [
    # Index
    path("", IndexView.as_view(), name="index"),
    # Show
    path("<int:pk>", ShowView.as_view(), name="show"),
    path("<slug:facility_slug>", ShowView.as_view(), name="show"),
    # Manage
    path("manage/", ManageView.as_view(), name="manage"),
    # Create
    path("new/", CreateView.as_view(), name="new"),
    # Update
    path("<int:pk>/update/", UpdateView.as_view(), name="update"),
    path("<slug:facility_slug>/update/", UpdateView.as_view(), name="update"),
    # Delete
    path("<int:pk>/delete/", DeleteView.as_view(), name="delete"),
    path("<slug:facility_slug>/delete/", DeleteView.as_view(), name="delete"),
    # SubURLs
    path(
        "<slug:facility_slug>/departments/",
        include("facility.urls.department", namespace="departments"),
    ),
    path(
        "<slug:facility_slug>/classes/",
        include("course.urls.facility_class", namespace="classes"),
    ),
    path(
        "<slug:facility_slug>/quarters/",
        include("facility.urls.quarters", namespace="quarters"),
    ),
    path(
        "<slug:facility_slug>/faculty/",
        include("facility.urls.faculty", namespace="faculty"),
    ),
    path(
        "<slug:facility_slug>/enrollments/",
        include("enrollment.urls.facility", namespace="enrollments"),
    )
]
