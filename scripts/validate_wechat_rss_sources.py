#!/usr/bin/env python3
"""Validate WeChat RSS sources configuration."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "同行资本市场内容系统" / "10_logs"


def load_config(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def validate_config(config: dict) -> tuple[dict, list[dict]]:
    issues = []
    sources = config.get("sources", [])
    enabled_count = sum(1 for s in sources if s.get("enabled", False))

    if "schema_version" not in config:
        issues.append({"severity": "ERROR", "field": "schema_version", "message": "schema_version is required"})

    if not sources:
        issues.append({"severity": "WARN", "field": "sources", "message": "No sources defined"})

    for idx, source in enumerate(sources):
        prefix = f"sources[{idx}]"
        if "source_id" not in source:
            issues.append({"severity": "ERROR", "field": f"{prefix}.source_id", "message": "source_id is required"})
        if "label" not in source:
            issues.append({"severity": "WARN", "field": f"{prefix}.label", "message": "label is recommended"})
        if "rss_url" not in source:
            issues.append({"severity": "ERROR", "field": f"{prefix}.rss_url", "message": "rss_url is required"})
        if "enabled" not in source:
            issues.append({"severity": "WARN", "field": f"{prefix}.enabled", "message": "enabled not set, defaulting to false"})

    return {
        "schema_version": config.get("schema_version", "unknown"),
        "source_count": len(sources),
        "enabled_count": enabled_count,
        "updated_at": config.get("updated_at", ""),
        "description": config.get("description", ""),
    }, issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate WeChat RSS sources configuration")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "config" / "wechat_rss_sources.yaml", help="Path to config file")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
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

    summary, issues = validate_config(config)

    error_count = sum(1 for i in issues if i["severity"] == "ERROR")
    warn_count = sum(1 for i in issues if i["severity"] == "WARN")

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "status": "PASS" if error_count == 0 else "FAILED",
        "summary": summary,
        "issues": issues,
        "error_count": error_count,
        "warn_count": warn_count,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run and args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
    elif not args.dry_run:
        output_path = OUTPUT_DIR / "latest_wechat_rss_source_validation.json"
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())