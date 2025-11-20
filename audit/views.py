from django.shortcuts import render


def dashboard(request):
    pages = [
        {"url": "/home", "issues": 5, "last_audit": "2025-11-19"},
        {"url": "/login", "issues": 0, "last_audit": "2025-11-18"},
        {"url": "/contact", "issues": 2, "last_audit": "2025-11-18"},
    ]

    total_pages = len(pages)
    total_issues = sum(p["issues"] for p in pages)

    context = {
        "active_page": "dashboard",
        "pages": pages,
        "total_pages": total_pages,
        "total_issues": total_issues,
        "last_audit": "Today",
    }
    return render(request, "audit/dashboard.html", context)


def pages_list(request):
    pages = [
        {"url": "/home", "issues": 5, "last_audit": "2025-11-19"},
        {"url": "/login", "issues": 0, "last_audit": "2025-11-18"},
        {"url": "/contact", "issues": 2, "last_audit": "2025-11-18"},
    ]
    context = {
        "active_page": "pages",
        "pages": pages,
    }
    return render(request, "audit/pages.html", context)


def new_audit(request):
    context = {
        "active_page": "new_audit",
    }
    return render(request, "audit/new_audit.html", context)


def history(request):
    audits = [
        {"date": "2025-11-19", "url": "/home", "issues": 5},
        {"date": "2025-11-18", "url": "/contact", "issues": 2},
        {"date": "2025-11-18", "url": "/login", "issues": 0},
    ]
    context = {
        "active_page": "history",
        "audits": audits,
    }
    return render(request, "audit/history.html", context)
