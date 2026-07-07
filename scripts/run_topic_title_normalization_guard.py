#!/usr/bin/env python3
"""Run topic title normalization guard."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "ignored"
TOPIC_CANDIDATES_DIR = REPO_ROOT / "同行资本市场内容系统" / "03_topic_candidates"


def load_config(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def is_metadata_title(title: str) -> bool:
    patterns = [
        r"^\[[^\]]+\]\s*$",
        r"^\([^)]+\)\s*$",
        r"^【[^】]+】\s*$",
        r"^[A-Za-z0-9_-]+$",
        r"^\d{4}-\d{2}-\d{2}",
        r"^[a-zA-Z]+/\d+",
        r"^[a-zA-Z]+_\d+",
        r"^[a-zA-Z]+\.\d+",
        r"^[a-zA-Z0-9_-]+\.html?$",
        r"^[a-zA-Z0-9_-]+\.json$",
    ]
    for pattern in patterns:
        if re.match(pattern, title.strip()):
            return True
    return False


def is_human_readable(title: str) -> bool:
    if not title or len(title.strip()) < 5:
        return False
    if len(title.strip()) > 200:
        return False
    char_count = len([c for c in title if '\u4e00' <= c <= '\u9fff'])
    return char_count >= 2


def normalize_title(title: str) -> str:
    title = title.strip()
    title = re.sub(r"\s+", " ", title)
    title = re.sub(r"[【】\[\]()<>《》]", "", title)
    title = title.strip()
    return title


def run_title_guard(topics: list, guards: dict) -> dict:
    reject_raw_metadata_title = guards.get("reject_raw_metadata_title", True)
    require_angle_for_repeated_event = guards.get("require_angle_for_repeated_event", True)
    require_human_readable_title = guards.get("require_human_readable_title", True)

    guard_results = []
    passed_count = 0
    failed_count = 0
    normalized_count = 0

    for topic in topics:
        topic_id = topic.get("topic_id", "")
        title = topic.get("title", "")
        normalized_title = topic.get("normalized_title", "") or normalize_title(title)
        is_repeated_event = topic.get("is_repeated_event", False)
        angle_info = topic.get("angle", {})
        has_angle = angle_info.get("type") is not None

        issues = []
        normalized = False

        if not normalized_title or normalized_title != title:
            normalized = True
            normalized_count += 1

        if reject_raw_metadata_title and is_metadata_title(title):
            issues.append({
                "type": "metadata_title",
                "severity": "REJECT",
                "message": "Title appears to be raw metadata format",
                "original_title": title,
            })

        if require_human_readable_title and not is_human_readable(title):
            issues.append({
                "type": "not_human_readable",
                "severity": "WARNING",
                "message": "Title may not be human readable",
                "title_length": len(title),
            })

        if require_angle_for_repeated_event and is_repeated_event and not has_angle:
            issues.append({
                "type": "missing_angle_for_repeated_event",
                "severity": "REJECT",
                "message": "Repeated event topic requires differentiated angle",
            })

        if normalized_title != title:
            issues.append({
                "type": "normalized",
                "severity": "INFO",
                "message": "Title was normalized",
                "original_title": title,
                "normalized_title": normalized_title,
            })

        is_rejected = any(i["severity"] == "REJECT" for i in issues)
        passed = not is_rejected

        if passed:
            passed_count += 1
        else:
            failed_count += 1

        guard_results.append({
            "topic_id": topic_id,
            "title": title,
            "normalized_title": normalized_title,
            "passed": passed,
            "is_rejected": is_rejected,
            "normalized": normalized,
            "issues": issues,
        })

    return {
        "summary": {
            "total_topics": len(topics),
            "passed_count": passed_count,
            "failed_count": failed_count,
            "normalized_count": normalized_count,
            "pass_rate": passed_count / len(topics) if len(topics) > 0 else 0.0,
        },
        "guard_rules": {
            "reject_raw_metadata_title": reject_raw_metadata_title,
            "require_angle_for_repeated_event": require_angle_for_repeated_event,
            "require_human_readable_title": require_human_readable_title,
        },
        "guard_results": guard_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run topic title normalization guard")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "config" / "topic_diversity_policy.yaml", help="Path to config file")
    parser.add_argument("--input", type=Path, default=None, help="Input topic candidates JSON file")
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

    guards = config.get("guards", {})

    if args.input:
        try:
            topic_candidates = load_json(args.input)
        except Exception as e:
            result = {
                "schema_version": "v1",
                "generated_at": datetime.now().isoformat(),
                "status": "FAILED",
                "error": f"Failed to load input file: {e}",
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 1
    else:
        latest_topics_file = TOPIC_CANDIDATES_DIR / "latest_daily_main_topic_selection.json"
        if latest_topics_file.exists():
            topic_candidates = load_json(latest_topics_file)
        else:
            topic_candidates = {"selected_topics": []}

    topics = topic_candidates.get("selected_topics", []) or topic_candidates.get("topics", [])

    guard_data = run_title_guard(topics, guards)

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "status": "SUCCESS",
        "dry_run": args.dry_run,
        **guard_data,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_topic_title_normalization_guard.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_topic_title_normalization_guard.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())