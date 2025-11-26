from django.contrib import admin
from .models import WebPage, AuditRecord


@admin.register(WebPage)
class WebPageAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "last_audit", "issues")
    search_fields = ("name", "url")


@admin.register(AuditRecord)
class AuditRecordAdmin(admin.ModelAdmin):
    list_display = ("page", "tool", "run_at", "issues_found")
    list_filter = ("tool", "run_at")
    search_fields = ("page__name", "page__url")