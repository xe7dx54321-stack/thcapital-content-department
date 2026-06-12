#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_fallback_strategy import load_fallback_strategies, summarize_fallback_strategies
from content_system.acquisition_playbook_common import basic_markdown, write_latest_report
from content_system.paths import get_project_paths


def main() -> int:
    strategies = load_fallback_strategies(ROOT)
    summary = summarize_fallback_strategies(strategies)
    payload = {"schema_version": "v1", "strategies": strategies, "summary": summary}
    write_latest_report(get_project_paths(ROOT), ROOT, "acquisition_fallback_strategies", payload, basic_markdown("Acquisition Fallback Strategies", summary))
    print(
        "acquisition-fallback-strategies-build "
        f"strategy_count={summary.get('strategy_count', 0)} primary_source_required={summary.get('primary_source_required', 0)} "
        f"second_source_required={summary.get('second_source_required', 0)} manual_review_required={summary.get('manual_review_required', 0)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
