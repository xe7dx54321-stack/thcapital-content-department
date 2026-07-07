#!/usr/bin/env python3
"""Apply differentiated angle boost to topic scores."""

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


def apply_angle_boosts(topics: list, angle_config: dict, topic_diversity_policy: dict) -> dict:
    boost_rules = angle_config.get("boost_rules", {})
    penalty_rules = angle_config.get("penalty_rules", {})
    boosts = topic_diversity_policy.get("boosts", {})

    strong_differentiated_angle_boost = boost_rules.get("strong_differentiated_angle", {}).get("boost_score", 0.12)
    fresh_undercovered_angle_boost = boost_rules.get("fresh_undercovered_angle", {}).get("boost_score", 0.10)
    multi_source_support_boost = boosts.get("multi_source_support", 0.08)
    weak_differentiation_penalty = penalty_rules.get("weak_differentiation", {}).get("penalty_score", 0.12)

    high_confidence_threshold = angle_config.get("angle_confidence_thresholds", {}).get("high", 0.75)
    medium_confidence_threshold = angle_config.get("angle_confidence_thresholds", {}).get("medium", 0.50)
    low_confidence_threshold = angle_config.get("angle_confidence_thresholds", {}).get("low", 0.25)

    boost_results = []
    total_boost_count = 0
    total_penalty_count = 0

    for topic in topics:
        topic_id = topic.get("topic_id", "")
        score = topic.get("score", 0)
        applied_boosts = []
        applied_penalties = []
        total_boost = 0.0
        total_penalty = 0.0

        angle_info = topic.get("angle", {})
        angle_confidence = angle_info.get("confidence", 0)
        angle_type = angle_info.get("type", "")

        if angle_confidence >= high_confidence_threshold and angle_type:
            applied_boosts.append({
                "type": "strong_differentiated_angle",
                "boost": strong_differentiated_angle_boost,
                "angle_type": angle_type,
                "confidence": angle_confidence,
                "reason": f"High confidence angle ({angle_type}) with confidence {angle_confidence}",
            })
            total_boost += strong_differentiated_angle_boost
            total_boost_count += 1

        elif angle_confidence >= medium_confidence_threshold and angle_type:
            applied_boosts.append({
                "type": "fresh_undercovered_angle",
                "boost": fresh_undercovered_angle_boost,
                "angle_type": angle_type,
                "confidence": angle_confidence,
                "reason": f"Medium confidence angle ({angle_type}) with confidence {angle_confidence}",
            })
            total_boost += fresh_undercovered_angle_boost
            total_boost_count += 1

        elif angle_confidence <= low_confidence_threshold:
            applied_penalties.append({
                "type": "weak_differentiation",
                "penalty": weak_differentiation_penalty,
                "reason": f"Weak angle differentiation with confidence {angle_confidence}",
            })
            total_penalty += weak_differentiation_penalty
            total_penalty_count += 1

        if topic.get("multi_source_support", False):
            source_count = topic.get("source_count", 0)
            if source_count >= 2:
                applied_boosts.append({
                    "type": "multi_source_support",
                    "boost": multi_source_support_boost,
                    "source_count": source_count,
                    "reason": f"Supported by {source_count} sources",
                })
                total_boost += multi_source_support_boost
                total_boost_count += 1

        adjusted_score = score + total_boost - total_penalty

        boost_results.append({
            "topic_id": topic_id,
            "title": topic.get("title", ""),
            "original_score": score,
            "total_boost": total_boost,
            "total_penalty": total_penalty,
            "adjusted_score": adjusted_score,
            "boost_applied": len(applied_boosts) > 0,
            "penalty_applied": len(applied_penalties) > 0,
            "boosts": applied_boosts,
            "penalties": applied_penalties,
            "angle_info": angle_info,
        })

    return {
        "summary": {
            "total_topics": len(topics),
            "total_boost_applications": total_boost_count,
            "total_penalty_applications": total_penalty_count,
            "topics_with_boosts": len([r for r in boost_results if r["boost_applied"]]),
            "topics_with_penalties": len([r for r in boost_results if r["penalty_applied"]]),
        },
        "boost_rules": {
            "strong_differentiated_angle": strong_differentiated_angle_boost,
            "fresh_undercovered_angle": fresh_undercovered_angle_boost,
            "multi_source_support": multi_source_support_boost,
            "weak_differentiation_penalty": weak_differentiation_penalty,
        },
        "confidence_thresholds": {
            "high": high_confidence_threshold,
            "medium": medium_confidence_threshold,
            "low": low_confidence_threshold,
        },
        "boost_results": boost_results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply differentiated angle boost")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "config" / "differentiated_angle_policy.yaml", help="Path to angle policy config")
    parser.add_argument("--diversity-policy", type=Path, default=REPO_ROOT / "config" / "topic_diversity_policy.yaml", help="Path to diversity policy config")
    parser.add_argument("--input", type=Path, default=None, help="Input topic candidates JSON file")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument("--output", type=Path, default=None, help="Output JSON file path")
    args = parser.parse_args()

    try:
        angle_config = load_config(args.config)
    except Exception as e:
        result = {
            "schema_version": "v1",
            "generated_at": datetime.now().isoformat(),
            "status": "FAILED",
            "error": str(e),
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    try:
        topic_diversity_policy = load_config(args.diversity_policy)
    except Exception as e:
        result = {
            "schema_version": "v1",
            "generated_at": datetime.now().isoformat(),
            "status": "FAILED",
            "error": f"Failed to load diversity policy: {e}",
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

    boost_data = apply_angle_boosts(topics, angle_config, topic_diversity_policy)

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "status": "SUCCESS",
        "dry_run": args.dry_run,
        **boost_data,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_differentiated_angle_boost.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_differentiated_angle_boost.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())