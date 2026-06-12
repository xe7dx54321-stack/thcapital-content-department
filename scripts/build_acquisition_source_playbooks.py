#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_playbook_common import basic_markdown, write_latest_report
from content_system.acquisition_source_playbook import load_source_playbooks, summarize_source_playbooks
from content_system.paths import get_project_paths


def main() -> int:
    sources = load_source_playbooks(ROOT)
    summary = summarize_source_playbooks(sources)
    payload = {"schema_version": "v1", "sources": sources, "summary": summary}
    write_latest_report(get_project_paths(ROOT), ROOT, "acquisition_source_playbooks", payload, basic_markdown("Acquisition Source Playbooks", summary))
    print(
        "acquisition-source-playbooks-build "
        f"source_count={summary.get('source_count', 0)} metadata_sources={summary.get('metadata_sources', 0)} "
        f"manual_only_sources={summary.get('manual_only_sources', 0)} disabled_sources={summary.get('disabled_sources', 0)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
