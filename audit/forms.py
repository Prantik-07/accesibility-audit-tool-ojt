from django import forms
from .models import WebPage, AuditRecord


class WebPageForm(forms.ModelForm):
    class Meta:
        model = WebPage
        fields = ['name', 'url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'url': forms.URLInput(attrs={'class': 'w-full px-3 py-2 border rounded'}),
        }


class AuditRecordForm(forms.ModelForm):
    class Meta:
        model = AuditRecord
        fields = ['page', 'tool', 'notes']
        widgets = {
            'page': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'tool': forms.Select(attrs={'class': 'w-full px-3 py-2 border rounded'}),
            'notes': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded', 'rows': 4}),
        }
