from django.db import models


class WebPage(models.Model):
    name = models.CharField(max_length=100)  # e.g. Home page
    url = models.CharField(max_length=255)   # e.g. /home or full URL
    last_audit = models.DateTimeField(null=True, blank=True)
    issues = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.url})"


class AuditRecord(models.Model):
    TOOL_CHOICES = [
        ("manual", "Manual"),
        ("axe", "axe-core"),
        ("pa11y", "pa11y"),
        ("lighthouse", "Lighthouse"),
    ]

    page = models.ForeignKey(WebPage, on_delete=models.CASCADE, related_name="audits")
    run_at = models.DateTimeField(auto_now_add=True)
    tool = models.CharField(max_length=20, choices=TOOL_CHOICES, default="manual")
    issues_found = models.IntegerField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Audit for {self.page.url} at {self.run_at:%Y-%m-%d %H:%M}"
