# facility/urls/faculty.py

from django.urls import path

from ..views.faculty import (
    IndexView,
    ShowView,
    CreateView,
    UpdateView,
    DeleteView,
    ManageView,
    DashboardView,
)

app_name = "facultys"

urlpatterns = [
    # Index
    path("", IndexView.as_view(), name="index"),
    # Dashboard
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # Manage faculty list (restricted to current user's facility)
    path("manage/", ManageView.as_view(), name="manage"),
    # Show
    path("<int:pk>", ShowView.as_view(), name="show"),
    path("<slug:faculty_slug>/", ShowView.as_view(), name="show"),
    # Create
    path("new/", CreateView.as_view(), name="new"),
    # Update
    path("<int:pk>/update/", UpdateView.as_view(), name="edit"),
    path("<slug:faculty_slug>/update/", UpdateView.as_view(), name="edit"),
    # Delete
    path("<int:pk>/delete/", DeleteView.as_view(), name="delete"),
    path("<slug:faculty_slug>/delete/", DeleteView.as_view(), name="delete"),
    
    
]
