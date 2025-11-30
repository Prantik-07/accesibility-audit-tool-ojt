import subprocess
import json
from django.utils import timezone
from .models import AuditRecord, WCAGIssue


def run_pa11y_audit(page):
    """
    Run pa11y audit on a given page URL
    Returns the audit record with issues
    """
    try:
        # Run pa11y command with proper error handling
        result = subprocess.run(
            ['pa11y', '--reporter', 'json', page.url],
            capture_output=True,
            text=True,
            timeout=60,
            shell=True  # Added for Windows compatibility
        )
        
        # Parse JSON output
        issues_data = []
        if result.stdout:
            try:
                issues_data = json.loads(result.stdout)
            except json.JSONDecodeError:
                # If JSON parsing fails, create audit with error
                audit = AuditRecord.objects.create(
                    page=page,
                    tool='pa11y',
                    issues_found=0,
                    notes=f'Pa11y output was not valid JSON. Output: {result.stdout[:200]}'
                )
                page.last_audit = timezone.now()
                page.issues = 0
                page.save()
                return audit
        
        # Create audit record
        audit = AuditRecord.objects.create(
            page=page,
            tool='pa11y',
            issues_found=len(issues_data),
            raw_json=issues_data if issues_data else None
        )
        
        # Create WCAG issues
        for issue in issues_data:
            WCAGIssue.objects.create(
                audit=audit,
                code=issue.get('code', 'Unknown'),
                wcag=issue.get('wcag', ''),
                message=issue.get('message', 'No message'),
                selector=issue.get('selector', ''),
                context=issue.get('context', ''),
                type=issue.get('type', 'error'),
                impact=issue.get('impact', '')
            )
        
        # Update page
        page.last_audit = timezone.now()
        page.issues = len(issues_data)
        page.save()
        
        return audit
        
    except subprocess.TimeoutExpired:
        # Create audit with timeout error
        audit = AuditRecord.objects.create(
            page=page,
            tool='pa11y',
            issues_found=0,
            notes='Audit timed out after 60 seconds. The page may be too slow or unreachable.'
        )
        page.last_audit = timezone.now()
        page.issues = 0
        page.save()
        return audit
        
    except FileNotFoundError:
        # Pa11y not found
        audit = AuditRecord.objects.create(
            page=page,
            tool='pa11y',
            issues_found=0,
            notes='Pa11y is not installed. Please install it with: npm install -g pa11y'
        )
        page.last_audit = timezone.now()
        page.issues = 0
        page.save()
        return audit
        
    except Exception as e:
        # Create audit with error note
        audit = AuditRecord.objects.create(
            page=page,
            tool='pa11y',
            issues_found=0,
            notes=f'Error running pa11y: {str(e)}'
        )
        page.last_audit = timezone.now()
        page.issues = 0
        page.save()
        return audit
