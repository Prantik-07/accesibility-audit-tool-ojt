import json
from pathlib import Path
from typing import Dict, Any

def run_axe(url: str) -> Dict[str, Any]:
    """
    Minimal stub that simulates an accessibility scan.
    Later, replace this with Playwright + axe-core results.
    """
    report = {
        "meta": {"url": url},
        "results": []
    }

    try:
        Path("audit/last_report.json").write_text(json.dumps(report, indent=2))
    except Exception:
        pass

    return report
