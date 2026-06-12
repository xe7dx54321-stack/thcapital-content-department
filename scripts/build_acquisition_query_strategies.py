#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from content_system.acquisition_playbook_common import basic_markdown, write_latest_report
from content_system.acquisition_query_strategy import load_query_strategies, summarize_query_strategies
from content_system.paths import get_project_paths


def main() -> int:
    strategies = load_query_strategies(ROOT)
    summary = summarize_query_strategies(strategies)
    payload = {"schema_version": "v1", "strategies": strategies, "summary": summary}
    write_latest_report(get_project_paths(ROOT), ROOT, "acquisition_query_strategies", payload, basic_markdown("Acquisition Query Strategies", summary))
    print(
        "acquisition-query-strategies-build "
        f"strategy_count={summary.get('strategy_count', 0)} keyword_count={summary.get('keyword_count', 0)} "
        f"expansion_trigger_count={summary.get('expansion_trigger_count', 0)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
