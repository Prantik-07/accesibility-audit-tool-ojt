from django.urls import path
from . import views

app_name = "audit"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("pages/", views.pages_list, name="pages"),
    path("new-audit/", views.new_audit, name="new_audit"),
    path("history/", views.history, name="history"),
]
