from django.shortcuts import render

def dashboard(request):
    return render(request, "audit/dashboard.html")

def pages_list(request):
    return render(request, "audit/pages.html")

def new_audit(request):
    return render(request, "audit/new_audit.html")

def history(request):
    return render(request, "audit/history.html")
