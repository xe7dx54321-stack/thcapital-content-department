#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.openclaw_acquisition_semantics_audit import build_openclaw_acquisition_semantics_audit
from content_system.paths import get_project_paths


def main() -> int:
    payload, _ = build_openclaw_acquisition_semantics_audit(get_project_paths(ROOT), ROOT)
    summary = payload.get("summary", {})
    print(
        "openclaw-acquisition-semantics-audit "
        f"acquisition_job_count={summary.get('acquisition_job_count', 0)} "
        f"high_value_playbook_jobs={summary.get('high_value_playbook_jobs', 0)} "
        f"medium_value_playbook_jobs={summary.get('medium_value_playbook_jobs', 0)} "
        f"do_not_migrate_jobs={summary.get('do_not_migrate_jobs', 0)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
