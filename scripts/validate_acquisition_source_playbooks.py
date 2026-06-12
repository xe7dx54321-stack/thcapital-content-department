#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_playbook_common import write_latest_report
from content_system.acquisition_source_playbook import render_source_playbook_validation, validate_source_playbooks
from content_system.paths import get_project_paths


def main() -> int:
    payload = validate_source_playbooks(ROOT)
    write_latest_report(get_project_paths(ROOT), ROOT, "acquisition_source_playbooks_validation", payload, render_source_playbook_validation(payload))
    print(
        "acquisition-source-playbooks-validate "
        f"status={payload.get('status')} source_count={payload.get('source_count', 0)} "
        f"metadata_sources={payload.get('metadata_sources', 0)} manual_only_sources={payload.get('manual_only_sources', 0)}"
    )
    return 0 if payload.get("status") in {"PASS", "ACTIONABLE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
