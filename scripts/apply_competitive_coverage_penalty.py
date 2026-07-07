#!/usr/bin/env python3
"""Apply competitive coverage penalty to topic scores."""

from __future__ import annotations

import argparse
import json
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


def apply_penalties(topics: list, config: dict, similarity_scores: list = None, diversity_scores: list = None) -> dict:
    penalties = config.get("penalties", {})
    recent_topic_duplicate_penalty = penalties.get("recent_topic_duplicate", 0.18)
    same_source_repetition_penalty = penalties.get("same_source_repetition", 0.10)
    same_lane_repetition_penalty = penalties.get("same_lane_repetition", 0.08)
    high_competitive_same_angle_penalty = penalties.get("high_competitive_same_angle", 0.14)

    similarity_score_map = {}
    if similarity_scores:
        for s in similarity_scores:
            similarity_score_map[s["topic_id"]] = s

    diversity_score_map = {}
    if diversity_scores:
        for d in diversity_scores:
            diversity_score_map[d["topic_id"]] = d

    penalty_results = []
    total_penalty_count = 0

    for topic in topics:
        topic_id = topic.get("topic_id", "")
        score = topic.get("score", 0)
        applied_penalties = []
        total_penalty = 0.0

        if similarity_score_map.get(topic_id, {}).get("is_duplicate", False):
            applied_penalties.append({
                "type": "recent_topic_duplicate",
                "penalty": recent_topic_duplicate_penalty,
                "reason": "Topic is similar to recent historical topic",
            })
            total_penalty += recent_topic_duplicate_penalty
            total_penalty_count += 1

        if diversity_score_map.get(topic_id):
            div_score = diversity_score_map[topic_id]
            if div_score.get("source_repetition_penalty", 0) > 0:
                applied_penalties.append({
                    "type": "same_source_repetition",
                    "penalty": div_score["source_repetition_penalty"],
                    "reason": f"Source {div_score['source']} has {div_score['source_count']} topics",
                })
                total_penalty += div_score["source_repetition_penalty"]
                total_penalty_count += 1

            if div_score.get("lane_repetition_penalty", 0) > 0:
                applied_penalties.append({
                    "type": "same_lane_repetition",
                    "penalty": div_score["lane_repetition_penalty"],
                    "reason": f"Lane {div_score['lane']} has {div_score['lane_count']} topics",
                })
                total_penalty += div_score["lane_repetition_penalty"]
                total_penalty_count += 1

        if topic.get("competitive_coverage", {}).get("high_coverage", False):
            applied_penalties.append({
                "type": "high_competitive_same_angle",
                "penalty": high_competitive_same_angle_penalty,
                "reason": "High competitive coverage on same angle",
            })
            total_penalty += high_competitive_same_angle_penalty
            total_penalty_count += 1

        adjusted_score = max(0, score - total_penalty)

        penalty_results.append({
            "topic_id": topic_id,
            "title": topic.get("title", ""),
            "original_score": score,
            "total_penalty": total_penalty,
            "adjusted_score": adjusted_score,
            "penalty_applied": len(applied_penalties) > 0,
            "penalties": applied_penalties,
        })

    return {
        "summary": {
            "total_topics": len(topics),
            "total_penalty_applications": total_penalty_count,
            "topics_with_penalties": len([r for r in penalty_results if r["penalty_applied"]]),
        },
        "penalty_rules": {
            "recent_topic_duplicate": recent_topic_duplicate_penalty,
            "same_source_repetition": same_source_repetition_penalty,
            "same_lane_repetition": same_lane_repetition_penalty,
            "high_competitive_same_angle": high_competitive_same_angle_penalty,
        },
        "penalty_results": penalty_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply competitive coverage penalty")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "config" / "topic_diversity_policy.yaml", help="Path to config file")
    parser.add_argument("--similarity", type=Path, default=OUTPUT_DIR / "latest_topic_similarity_report.json", help="Path to similarity report")
    parser.add_argument("--diversity", type=Path, default=OUTPUT_DIR / "latest_source_lane_diversity.json", help="Path to diversity report")
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

    similarity_scores = []
    if args.similarity.exists():
        try:
            similarity_data = load_json(args.similarity)
            similarity_scores = similarity_data.get("similarity_scores", [])
        except Exception:
            pass

    diversity_scores = []
    if args.diversity.exists():
        try:
            diversity_data = load_json(args.diversity)
            diversity_scores = diversity_data.get("topic_diversity_scores", [])
        except Exception:
            pass

    penalty_data = apply_penalties(topics, config, similarity_scores, diversity_scores)

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "status": "SUCCESS",
        "dry_run": args.dry_run,
        **penalty_data,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_competitive_coverage_penalty.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_competitive_coverage_penalty.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())