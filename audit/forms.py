from django import forms
from .models import WebPage, AuditRecord


class WebPageForm(forms.ModelForm):
    class Meta:
        model = WebPage
        fields = ["name", "url"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "w-full border rounded px-3 py-2 text-sm"}
            ),
            "url": forms.TextInput(
                attrs={"class": "w-full border rounded px-3 py-2 text-sm"}
            ),
        }


class AuditRecordForm(forms.ModelForm):
    class Meta:
        model = AuditRecord
        fields = ["page", "tool", "issues_found", "notes"]
        widgets = {
            "page": forms.Select(
                attrs={"class": "w-full border rounded px-3 py-2 text-sm"}
            ),
            "tool": forms.Select(
                attrs={"class": "w-full border rounded px-3 py-2 text-sm"}
            ),
            "issues_found": forms.NumberInput(
                attrs={"class": "w-full border rounded px-3 py-2 text-sm"}
            ),
            "notes": forms.Textarea(
                attrs={
                    "class": "w-full border rounded px-3 py-2 text-sm",
                    "rows": 3,
                }
            ),
        }
