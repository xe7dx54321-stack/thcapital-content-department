#!/usr/bin/env python3
"""Run WeChat intelligence integration for Phase 34A."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "同行资本市场内容系统" / "14_wechat_rss"


def load_config(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def integrate_intelligence(config: dict, dry_run: bool) -> dict:
    integrated_topics = []
    integrated_evidence = []
    integration_errors = []

    return {
        "total_topics": 0,
        "integrated_topics_count": len(integrated_topics),
        "integrated_evidence_count": len(integrated_evidence),
        "integration_errors_count": len(integration_errors),
        "integrated_topics": integrated_topics,
        "integrated_evidence": integrated_evidence,
        "integration_errors": integration_errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run WeChat intelligence integration")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "config" / "wechat_rss_sources.yaml", help="Path to config file")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument("--input", type=Path, default=None, help="Input JSON file path")
    parser.add_argument("--output", type=Path, default=None, help="Output JSON file path")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
    except Exception as e:
        result = {
            "schema_version": "v1",
            "generated_at": datetime.now().isoformat(),
            "status": "FAILED",
            "error": str(e),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    summary = integrate_intelligence(config, args.dry_run)

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "status": "SUCCESS" if summary["integration_errors_count"] == 0 else "PARTIAL",
        "dry_run": args.dry_run,
        "summary": summary,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_wechat_integration.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_wechat_integration.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())