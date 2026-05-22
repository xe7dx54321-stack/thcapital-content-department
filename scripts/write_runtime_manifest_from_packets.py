#!/usr/bin/env python3
"""Write a runtime manifest JSON from existing source packet artifacts.

This command is intentionally an adapter. It does not run fetchers, does not
retry sources, and does not change existing packet/top20/manifest outputs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT_CANDIDATE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT_CANDIDATE / "src"))

from content_system.paths import get_project_paths  # noqa: E402
from content_system.runtime_manifest import manifest_to_dict, validate_runtime_manifest  # noqa: E402
from content_system.runtime_manifest_writer import (  # noqa: E402
    build_runtime_manifest_from_packet_dir,
    default_latest_runtime_manifest_output,
    default_runtime_manifest_output,
    discover_latest_source_packet_dir,
    load_default_registry,
    write_runtime_manifest,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build runtime manifest from source packet artifacts.")
    parser.add_argument("--source-packets-dir", type=Path, default=None, help="Directory containing source packet JSON files.")
    parser.add_argument("--output", type=Path, default=None, help="Output runtime manifest JSON path.")
    parser.add_argument("--latest-output", type=Path, default=None, help="Optional latest runtime manifest JSON path.")
    parser.add_argument("--no-latest", action="store_true", help="Do not write latest_runtime_manifest.json.")
    parser.add_argument("--pipeline-name", default="source_packets_adapter", help="Pipeline name to store in the manifest.")
    parser.add_argument("--script-name", default="write_runtime_manifest_from_packets.py", help="Script name to store in the manifest.")
    parser.add_argument("--run-date", default=None, help="Run date, YYYY-MM-DD. Inferred from packet directory when omitted.")
    parser.add_argument("--json", action="store_true", help="Print compact JSON summary.")
    parser.add_argument("--allow-errors", action="store_true", help="Return 0 even when manifest validation has ERROR issues.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = get_project_paths(REPO_ROOT_CANDIDATE)
    source_packets_dir = args.source_packets_dir or discover_latest_source_packet_dir(paths.market_content_root)

    if source_packets_dir is None:
        print("No source packet directory found. Nothing to convert.")
        return 0

    registry = load_default_registry(paths.repo_root)
    manifest = build_runtime_manifest_from_packet_dir(
        source_packets_dir,
        registry=registry,
        repo_root=paths.repo_root,
        run_date=args.run_date,
        pipeline_name=args.pipeline_name,
        script_name=args.script_name,
    )

    issues = validate_runtime_manifest(manifest, registry=registry)
    errors = sum(1 for issue in issues if issue.severity == "ERROR")
    warnings = sum(1 for issue in issues if issue.severity == "WARN")

    output = args.output or default_runtime_manifest_output(manifest.run_date, paths.repo_root)
    write_runtime_manifest(manifest, output)

    latest_output = args.latest_output or default_latest_runtime_manifest_output(paths.repo_root)
    if not args.no_latest:
        write_runtime_manifest(manifest, latest_output)

    summary = {
        "source_packets_dir": str(source_packets_dir),
        "output": str(output),
        "latest_output": None if args.no_latest else str(latest_output),
        "run_id": manifest.run_id,
        "status": manifest.status,
        "sources": manifest.source_count,
        "items_found": manifest.total_items_found,
        "items_written": manifest.total_items_written,
        "errors": errors,
        "warnings": warnings,
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("Runtime Manifest Writer")
        print("=======================")
        for key, value in summary.items():
            print(f"{key}: {value}")
        if issues:
            print("\nIssues:")
            for issue in issues[:20]:
                source = f" [{issue.source_id}]" if issue.source_id else ""
                print(f"- {issue.severity}{source} {issue.field}: {issue.message}")
            if len(issues) > 20:
                print(f"... {len(issues) - 20} more issues")

    if errors and not args.allow_errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
