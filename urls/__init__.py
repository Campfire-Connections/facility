# facility/urls/__init__.py

from django.urls import path, include

urlpatterns = [
    path("facilities/", include("facility.urls.facility")),
    path("quarters/", include("facility.urls.quarters")),
    path("departments/", include("facility.urls.department")),
]
