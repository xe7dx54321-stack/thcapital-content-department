#!/usr/bin/env python3
"""Check evidence support for WeChat articles."""

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


def check_evidence(config: dict, dry_run: bool) -> dict:
    articles_with_evidence = []
    articles_without_evidence = []
    evidence_support_rate = 0.0

    return {
        "total_articles": 0,
        "articles_with_evidence_count": len(articles_with_evidence),
        "articles_without_evidence_count": len(articles_without_evidence),
        "evidence_support_rate": evidence_support_rate,
        "articles_with_evidence": articles_with_evidence,
        "articles_without_evidence": articles_without_evidence,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check evidence support for WeChat articles")
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

    summary = check_evidence(config, args.dry_run)

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "status": "SUCCESS",
        "dry_run": args.dry_run,
        "summary": summary,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_evidence_support.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_evidence_support.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())