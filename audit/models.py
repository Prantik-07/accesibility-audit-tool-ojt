from django.db import models


class WebPage(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255)
    last_audit = models.DateTimeField(null=True, blank=True)
    issues = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.url})"


class AuditRecord(models.Model):
    TOOL_CHOICES = [
        ("manual", "Manual"),
        ("pa11y", "pa11y"),
    ]

    page = models.ForeignKey(WebPage, on_delete=models.CASCADE, related_name="audits")
    run_at = models.DateTimeField(auto_now_add=True)
    tool = models.CharField(max_length=20, choices=TOOL_CHOICES, default="manual")
    issues_found = models.IntegerField()
    notes = models.TextField(blank=True)
    raw_json = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Audit for {self.page.url} at {self.run_at:%Y-%m-%d %H:%M}"


class WCAGIssue(models.Model):
    audit = models.ForeignKey(
        AuditRecord, on_delete=models.CASCADE, related_name="wcag_issues"
    )
    code = models.CharField(max_length=100)
    wcag = models.CharField(max_length=50, blank=True)
    message = models.TextField()
    selector = models.TextField(blank=True)
    context = models.TextField(blank=True)
    type = models.CharField(max_length=20, blank=True)
    impact = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.code} ({self.audit_id})"
