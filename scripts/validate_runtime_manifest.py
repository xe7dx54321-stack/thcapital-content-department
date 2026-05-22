#!/usr/bin/env python3
"""Validate a runtime manifest against the P0-008 contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.runtime_manifest import (  # noqa: E402
    default_manifest_path,
    load_runtime_manifest,
    summarize_manifest,
    validate_runtime_manifest,
)
from content_system.sources import load_source_registry  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate runtime manifest JSON files.")
    parser.add_argument(
        "manifest",
        nargs="?",
        type=Path,
        default=None,
        help="Manifest JSON path. Defaults to config/runtime_manifest_example.json.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable validation summary.")
    parser.add_argument("--no-registry", action="store_true", help="Skip validation against config/sources.yaml.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    manifest_path = args.manifest or default_manifest_path(REPO_ROOT)

    if not manifest_path.exists():
        print(f"Runtime manifest not found: {manifest_path}", file=sys.stderr)
        return 1

    manifest = load_runtime_manifest(manifest_path)
    registry = None if args.no_registry else load_source_registry(repo_root=REPO_ROOT)
    issues = validate_runtime_manifest(manifest, registry=registry)
    summary = summarize_manifest(manifest, issues)

    if args.json:
        payload = {
            "manifest_path": str(manifest_path.relative_to(REPO_ROOT) if manifest_path.is_relative_to(REPO_ROOT) else manifest_path),
            "summary": summary,
            "issues": [issue.__dict__ for issue in issues],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("Runtime Manifest Validation")
        print("===========================")
        print(f"manifest: {manifest_path}")
        print(f"schema_version: {summary['schema_version']}")
        print(f"run_id: {summary['run_id']}")
        print(f"run_date: {summary['run_date']}")
        print(f"pipeline: {summary['pipeline_name']}")
        print(f"script: {summary['script_name']}")
        print(f"status: {summary['status']}")
        print(f"sources: {summary['source_count']}")
        print(f"items_found: {summary['total_items_found']}")
        print(f"items_written: {summary['total_items_written']}")
        print("\nSource status distribution:")
        for status, count in summary["status_distribution"].items():
            if count:
                print(f"  {status}: {count}")
        print("\nIssues:")
        if not issues:
            print("  None")
        else:
            for issue in issues:
                source = f" source={issue.source_id}" if issue.source_id else ""
                print(f"  [{issue.severity}] {issue.field}:{source} {issue.message}")
        print("\nOK" if summary["errors"] == 0 else "\nFAILED")

    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
