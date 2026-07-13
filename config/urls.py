from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Frontend pages
    path("", include("frontend.urls")),
    # Backend APIs
    path("api/", include("accounts.urls")),
]