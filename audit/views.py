from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from django.http import HttpResponse
from django.template.loader import get_template

from .models import WebPage, AuditRecord
from .forms import WebPageForm, AuditRecordForm


def dashboard(request):
    total_pages = WebPage.objects.count()
    total_audits = AuditRecord.objects.count()
    total_issues = WebPage.objects.aggregate(
        total=models.Sum("issues")
    )["total"] or 0

    last_audit = AuditRecord.objects.order_by("-run_at").first()
    recent_pages = WebPage.objects.order_by("-last_audit")[:5]

    context = {
        "total_pages": total_pages,
        "total_audits": total_audits,
        "total_issues": total_issues,
        "last_audit": last_audit,
        "pages": recent_pages,
    }
    return render(request, "audit/dashboard.html", context)


def pages_list(request):
    pages = WebPage.objects.all().order_by("name")
    return render(request, "audit/pages.html", {"pages": pages})


def new_page(request):
    if request.method == "POST":
        form = WebPageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("audit:pages")
    else:
        form = WebPageForm()
    return render(request, "audit/new_page.html", {"form": form})


def new_audit(request):
    if request.method == "POST":
        form = AuditRecordForm(request.POST)
        if form.is_valid():
            audit = form.save(commit=False)
            audit.issues_found = 0  # Will be updated by pa11y
            audit.save()
            # Update WebPage summary
            page = audit.page
            page.last_audit = timezone.now()
            page.issues = audit.issues_found
            page.save()
            return redirect("audit:history")
    else:
        form = AuditRecordForm()
    return render(request, "audit/new_audit.html", {"form": form})


def audit_detail(request, audit_id):
    audit = get_object_or_404(AuditRecord, id=audit_id)
    issues = audit.wcag_issues.all()
    return render(request, "audit/audit_detail.html", {"audit": audit, "issues": issues})


def history(request):
    audits = AuditRecord.objects.select_related("page").order_by("-run_at")
    return render(request, "audit/history.html", {"audits": audits})
