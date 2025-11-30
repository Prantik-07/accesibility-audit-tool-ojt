import subprocess
import json
from .models import AuditRecord, WCAGIssue


def run_pa11y_audit(page):
    """
    Run pa11y audit on a given page URL
    Returns the audit record with issues
    """
    try:
        # Run pa11y command
        result = subprocess.run(
            ['pa11y', '--reporter', 'json', page.url],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse JSON output
        if result.stdout:
            issues_data = json.loads(result.stdout)
        else:
            issues_data = []
        
        # Create audit record
        audit = AuditRecord.objects.create(
            page=page,
            tool='pa11y',
            issues_found=len(issues_data),
            raw_json=issues_data
        )
        
        # Create WCAG issues
        for issue in issues_data:
            WCAGIssue.objects.create(
                audit=audit,
                code=issue.get('code', ''),
                wcag=issue.get('wcag', ''),
                message=issue.get('message', ''),
                selector=issue.get('selector', ''),
                context=issue.get('context', ''),
                type=issue.get('type', ''),
                impact=issue.get('impact', '')
            )
        
        # Update page
        page.issues = len(issues_data)
        page.save()
        
        return audit
        
    except subprocess.TimeoutExpired:
        # Create audit with error note
        audit = AuditRecord.objects.create(
            page=page,
            tool='pa11y',
            issues_found=0,
            notes='Audit timed out after 30 seconds'
        )
        return audit
        
    except Exception as e:
        # Create audit with error note
        audit = AuditRecord.objects.create(
            page=page,
            tool='pa11y',
            issues_found=0,
            notes=f'Error running pa11y: {str(e)}'
        )
        return audit
