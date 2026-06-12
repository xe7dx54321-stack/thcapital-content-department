#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_downstream_router import render_downstream_route_validation, validate_downstream_routes
from content_system.acquisition_playbook_common import write_latest_report
from content_system.paths import get_project_paths


def main() -> int:
    payload = validate_downstream_routes(ROOT)
    write_latest_report(get_project_paths(ROOT), ROOT, "acquisition_downstream_routes_validation", payload, render_downstream_route_validation(payload))
    print(f"acquisition-downstream-routes-validate status={payload.get('status')} route_count={payload.get('route_count', 0)}")
    return 0 if payload.get("status") in {"PASS", "ACTIONABLE"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
