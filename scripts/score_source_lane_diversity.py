#!/usr/bin/env python3
"""Score source and lane diversity for topic selection."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List

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


def calculate_diversity_score(
    topic_counts: Dict[str, int],
    total_topics: int,
) -> float:
    if total_topics == 0:
        return 0.0
    entropy = 0.0
    for count in topic_counts.values():
        probability = count / total_topics
        entropy -= probability * (probability ** -1 if probability == 0 else probability)
    max_entropy = len(topic_counts) ** 0.5 if len(topic_counts) > 0 else 0.0
    return entropy / max_entropy if max_entropy > 0 else 0.0


def score_source_lane_diversity(topics: List[dict]) -> dict:
    source_counts: Dict[str, int] = {}
    lane_counts: Dict[str, int] = {}
    source_lane_matrix: Dict[str, Dict[str, int]] = {}

    for topic in topics:
        source = topic.get("source", "unknown")
        lane = topic.get("lane", "unknown")

        source_counts[source] = source_counts.get(source, 0) + 1
        lane_counts[lane] = lane_counts.get(lane, 0) + 1

        if source not in source_lane_matrix:
            source_lane_matrix[source] = {}
        source_lane_matrix[source][lane] = source_lane_matrix[source].get(lane, 0) + 1

    total_topics = len(topics)
    source_diversity = calculate_diversity_score(source_counts, total_topics)
    lane_diversity = calculate_diversity_score(lane_counts, total_topics)

    overall_diversity = (source_diversity + lane_diversity) / 2.0

    topic_diversity_scores = []
    for topic in topics:
        source = topic.get("source", "unknown")
        lane = topic.get("lane", "unknown")

        source_count = source_counts.get(source, 1)
        lane_count = lane_counts.get(lane, 1)

        source_repetition_penalty = min(source_count - 1, 5) * 0.10
        lane_repetition_penalty = min(lane_count - 1, 5) * 0.08

        topic_diversity_scores.append({
            "topic_id": topic.get("topic_id", ""),
            "title": topic.get("title", ""),
            "source": source,
            "lane": lane,
            "source_count": source_count,
            "lane_count": lane_count,
            "source_repetition_penalty": source_repetition_penalty,
            "lane_repetition_penalty": lane_repetition_penalty,
            "total_diversity_penalty": source_repetition_penalty + lane_repetition_penalty,
        })

    return {
        "summary": {
            "total_topics": total_topics,
            "unique_sources": len(source_counts),
            "unique_lanes": len(lane_counts),
            "source_diversity_score": source_diversity,
            "lane_diversity_score": lane_diversity,
            "overall_diversity_score": overall_diversity,
        },
        "source_distribution": source_counts,
        "lane_distribution": lane_counts,
        "source_lane_matrix": source_lane_matrix,
        "topic_diversity_scores": topic_diversity_scores,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score source/lane diversity")
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

    diversity_data = score_source_lane_diversity(topics)

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "status": "SUCCESS",
        "dry_run": args.dry_run,
        "policy_config": {
            "same_source_repetition_penalty": config.get("penalties", {}).get("same_source_repetition", 0.10),
            "same_lane_repetition_penalty": config.get("penalties", {}).get("same_lane_repetition", 0.08),
        },
        **diversity_data,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_source_lane_diversity.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_source_lane_diversity.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())