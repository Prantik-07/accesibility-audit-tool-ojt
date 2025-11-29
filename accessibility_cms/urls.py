# accessibility_cms/urls.py
"""Project URL configuration.

Make sure this file is placed at the project level (same folder as settings.py).
This file redirects root '/' to the audit dashboard and includes the audit app routes.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Admin site
    path("admin/", admin.site.urls),

    # Audit app routes (keeps existing behavior: /dashboard/, /pages/, etc.)
    path("", include("audit.urls")),  # include at root so /dashboard/ etc. work

    # Redirect the empty root path '/' to the audit dashboard view
    # Use pattern_name so it follows the URL name from audit/urls.py
    path("", RedirectView.as_view(pattern_name="audit:dashboard", permanent=False)),

    # (Optional) If you want the audit app to live under /audit/ instead, use:
    # path("audit/", include("audit.urls")),
    # and change RedirectView pattern_name target to "audit:dashboard" accordingly.
]
