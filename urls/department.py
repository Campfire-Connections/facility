# facility/urls/department.py

from django.urls import path
from django.views.generic import RedirectView

from ..views.department import (
    IndexView,
    IndexByFacilityView,
    ShowView,
    CreateView,
    UpdateView,
    DeleteView,
)

app_name = "departments"

urlpatterns = [
    # Index
    path("", IndexByFacilityView.as_view(), name="index"),
    # Show
    path("<int:pk>", ShowView.as_view(), name="show"),
    path("<slug:department_slug>", ShowView.as_view(), name="show"),
    # Create
    path("new", RedirectView.as_view(pattern_name="departments:new", permanent=False)),
    path("new/", CreateView.as_view(), name="new"),
    # Update
    path("<int:pk>/update/", UpdateView.as_view(), name="edit"),
    path("<slug:department_slug>/update/", UpdateView.as_view(), name="edit"),
    # Delete
    path("<int:pk>/delete/", DeleteView.as_view(), name="delete"),
    path("<slug:department_slug>/delete/", DeleteView.as_view(), name="delete"),
]
