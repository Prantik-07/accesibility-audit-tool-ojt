from django.urls import path
from . import views

app_name = "audit"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("pages/", views.pages_list, name="pages"),
    path("pages/new/", views.new_page, name="new_page"),
    path("audits/new/", views.new_audit, name="new_audit"),
    path("audits/<int:audit_id>/", views.audit_detail, name="audit_detail"),
    path("history/", views.history, name="history"),
]
