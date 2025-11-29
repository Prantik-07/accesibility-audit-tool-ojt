from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET

from .models import WebPage, AuditRecord
from .forms import WebPageForm, AuditRecordForm
from .services import run_axe  # simple runner stub or your real runner


def dashboard(request):
    """
    Dashboard view:
    - total_pages: count of WebPage rows
    - total_audits: count of AuditRecord rows
    - total_issues: sum of issues_found across all audits (0 if none)
    - last_audit: most recent AuditRecord instance or None
    Renders: audit/dashboard.html with context
    """
    total_pages = WebPage.objects.count()
    total_audits = AuditRecord.objects.count()

    agg = AuditRecord.objects.aggregate(total=Sum("issues_found"))
    total_issues = agg.get("total") or 0

    last_audit = AuditRecord.objects.order_by("-run_at").first()

    context = {
        "total_pages": total_pages,
        "total_audits": total_audits,
        "total_issues": total_issues,
        "last_audit": last_audit,
    }
    return render(request, "audit/dashboard.html", context)


def pages_list(request):
    """
    List all pages.
    """
    pages = WebPage.objects.all().order_by("name")
    return render(request, "audit/pages.html", {"pages": pages})


def new_page(request):
    """
    Create a new WebPage via WebPageForm.
    """
    if request.method == "POST":
        form = WebPageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("audit:pages")
    else:
        form = WebPageForm()
    return render(request, "audit/new_page.html", {"form": form})


def new_audit(request):
    """
    Create a new AuditRecord via form (manual entry).
    After saving, update the related WebPage summary fields.
    """
    if request.method == "POST":
        form = AuditRecordForm(request.POST)
        if form.is_valid():
            audit = form.save()
            # Update related WebPage summary fields
            try:
                page = audit.page
                page.last_audit = timezone.now()
                # if audit.issues_found is present on the model
                if hasattr(audit, "issues_found"):
                    page.issues = audit.issues_found
                page.save(update_fields=["last_audit", "issues"])
            except Exception:
                # swallow exceptions to avoid breaking the flow
                pass
            return redirect("audit:history")
    else:
        form = AuditRecordForm()
    return render(request, "audit/new_audit.html", {"form": form})


def history(request):
    """
    Show audit history, newest first. Uses select_related to reduce queries.
    """
    audits = AuditRecord.objects.select_related("page").order_by("-run_at")
    return render(request, "audit/history.html", {"audits": audits})


@require_POST
def run_audit_view(request, page_id):
    """
    Trigger an accessibility audit for a WebPage.
    - Calls run_axe(url)
    - Creates AuditRecord storing raw JSON in `notes` (string) and updates issues_found
    - Updates WebPage.last_audit and WebPage.issues
    Returns JSON: {"audit_id": id, "issues_found": n}
    """
    page = get_object_or_404(WebPage, pk=page_id)
    url = page.url

    try:
        report = run_axe(url)
    except Exception as e:
        return JsonResponse({"error": "runner_error", "detail": str(e)}, status=500)

    results = report.get("results") if isinstance(report, dict) else []
    if not isinstance(results, list):
        results = []

    issues_count = len(results)

    # Create AuditRecord using existing model fields (adapt if your field names differ)
    audit = AuditRecord.objects.create(
        page=page,
        issues_found=issues_count,
        notes=json.dumps(report)
    )

    # Update WebPage fields (safe — fields exist in your model screenshot)
    page.last_audit = timezone.now()
    page.issues = issues_count
    page.save(update_fields=["last_audit", "issues"])

    return JsonResponse({"audit_id": audit.id, "issues_found": issues_count})


@require_GET
def page_detail_view(request, page_id):
    """
    Render page detail template that includes a Run Audit button and recent audits.
    """
    page = get_object_or_404(WebPage, pk=page_id)
    recent_audits = AuditRecord.objects.filter(page=page).order_by("-run_at")[:8]
    return render(request, "audit/page_detail.html", {"page": page, "audits": recent_audits})
