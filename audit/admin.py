from django.contrib import admin
from .models import WebPage, AuditRecord, WCAGIssue


@admin.register(WebPage)
class WebPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'issues', 'last_audit']
    search_fields = ['name', 'url']


@admin.register(AuditRecord)
class AuditRecordAdmin(admin.ModelAdmin):
    list_display = ['page', 'tool', 'issues_found', 'run_at']
    list_filter = ['tool', 'run_at']
    search_fields = ['page__name', 'page__url']


@admin.register(WCAGIssue)
class WCAGIssueAdmin(admin.ModelAdmin):
    list_display = ['code', 'wcag', 'type', 'impact', 'audit']
    list_filter = ['type', 'impact']
    search_fields = ['code', 'message']