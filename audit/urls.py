from django.urls import path
from . import views

app_name = "audit"

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("pages/", views.pages_list, name="pages"),
    path("pages/new/", views.new_page, name="new_page"),
    path("pages/<int:page_id>/", views.page_detail_view, name="page_detail"),
    path("pages/<int:page_id>/run_audit/", views.run_audit_view, name="run_audit"),
    path("audits/new/", views.new_audit, name="new_audit"),
    path("history/", views.history, name="history"),
]
