#!/usr/bin/env python3
"""Check runtime network readiness."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.runtime_network_readiness import write_network_readiness_report  # noqa: E402


def main() -> int:
    payload, _ = write_network_readiness_report(get_project_paths(ROOT), ROOT)
    print(json.dumps({k: payload.get(k) for k in ("status", "dns_ok", "international_source_ok", "domestic_source_ok")}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
