#!/usr/bin/env python3
"""Validate and summarize config/sources.yaml."""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))

from content_system.sources import SourceConfig, SourceRegistryError, load_source_registry, validate_registry  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate the TH Capital source registry.")
    parser.add_argument("--path", type=Path, default=None, help="Path to sources.yaml. Defaults to config/sources.yaml.")
    parser.add_argument("--list", action="store_true", help="List source entries after validation.")
    parser.add_argument("--tier", type=str, default=None, help="List only sources in this tier.")
    parser.add_argument("--category", type=str, default=None, help="List only sources in this category.")
    return parser.parse_args()


def print_distribution(title: str, counts: Counter[str], order: tuple[str, ...] | None = None) -> None:
    print(f"\n{title}:")
    keys = order or tuple(sorted(counts))
    for key in keys:
        if counts.get(key, 0):
            print(f"  {key}: {counts[key]}")


def source_rows(sources: tuple[SourceConfig, ...]) -> list[str]:
    rows = []
    for source in sources:
        enabled = "yes" if source.enabled else "no"
        rows.append(
            f"{source.source_id:<28} {source.tier:<2} {source.category:<20} "
            f"{source.language:<5} {enabled:<7} {source.fetch_method:<12} {source.label}"
        )
    return rows


def print_sources(sources: tuple[SourceConfig, ...]) -> None:
    print("\nSources:")
    print(f"{'source_id':<28} {'T':<2} {'category':<20} {'lang':<5} {'enabled':<7} {'method':<12} label")
    print("-" * 100)
    for row in source_rows(sources):
        print(row)


def print_issues(issues: tuple) -> tuple[int, int]:
    counts = Counter(issue.severity for issue in issues)
    error_count = counts.get("ERROR", 0)
    warn_count = counts.get("WARN", 0)
    print("\nIssues:")
    print(f"  ERROR: {error_count}")
    print(f"  WARN: {warn_count}")
    for issue in issues:
        source = issue.source_id or "<registry>"
        field = issue.field or "<unknown>"
        print(f"  {issue.severity}: {source}.{field}: {issue.message}")
    return error_count, warn_count


def main() -> int:
    args = parse_args()

    try:
        registry = load_source_registry(path=args.path, repo_root=REPO_ROOT)
    except (OSError, SourceRegistryError) as exc:
        print("Source Registry Validation")
        print("==========================")
        print(f"ERROR: failed to load registry: {exc}")
        return 1

    issues = validate_registry(registry)
    enabled = registry.enabled_sources()
    tier_counts = registry.tier_counts()
    category_counts = registry.category_counts()

    print("Source Registry Validation")
    print("==========================")
    print(f"schema_version: {registry.schema_version}")
    print(f"sources: {len(registry.sources)}")
    print(f"enabled: {len(enabled)}")

    print_distribution("Tier distribution", tier_counts, ("A", "B", "C", "D", "E"))
    print_distribution("Category distribution", category_counts)

    error_count, _warn_count = print_issues(issues)

    filtered_sources = registry.sources
    if args.tier:
        filtered_sources = registry.by_tier(args.tier)
    if args.category:
        filtered_sources = tuple(source for source in filtered_sources if source.category == args.category)

    if args.list or args.tier or args.category:
        print_sources(filtered_sources)

    if error_count:
        print("\nFAILED")
        return 1
    print("\nOK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
