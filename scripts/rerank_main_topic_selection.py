#!/usr/bin/env python3
"""Rerank main topic selection with diversity adjustments."""

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


def rerank_topics(
    topics: list,
    penalty_results: list,
    boost_results: list,
    guard_results: list,
) -> dict:
    penalty_map = {r["topic_id"]: r for r in penalty_results}
    boost_map = {r["topic_id"]: r for r in boost_results}
    guard_map = {r["topic_id"]: r for r in guard_results}

    reranked_topics = []
    rejected_topics = []

    for topic in topics:
        topic_id = topic.get("topic_id", "")
        original_score = topic.get("score", 0)

        penalty_result = penalty_map.get(topic_id, {})
        boost_result = boost_map.get(topic_id, {})
        guard_result = guard_map.get(topic_id, {})

        penalty_adjusted_score = penalty_result.get("adjusted_score", original_score)
        boost_adjusted_score = boost_result.get("adjusted_score", penalty_adjusted_score)

        final_score = boost_adjusted_score

        is_rejected = guard_result.get("is_rejected", False)
        normalized_title = guard_result.get("normalized_title", topic.get("title", ""))

        topic_entry = {
            "topic_id": topic_id,
            "title": topic.get("title", ""),
            "normalized_title": normalized_title,
            "source": topic.get("source", ""),
            "lane": topic.get("lane", ""),
            "original_score": original_score,
            "penalty_adjusted_score": penalty_adjusted_score,
            "boost_adjusted_score": boost_adjusted_score,
            "final_score": final_score,
            "is_rejected": is_rejected,
            "rejection_reasons": guard_result.get("issues", []) if is_rejected else [],
            "penalties": penalty_result.get("penalties", []),
            "boosts": boost_result.get("boosts", []),
            "metadata": topic.get("metadata", {}),
        }

        if is_rejected:
            rejected_topics.append(topic_entry)
        else:
            reranked_topics.append(topic_entry)

    reranked_topics.sort(key=lambda x: x["final_score"], reverse=True)

    for idx, topic in enumerate(reranked_topics):
        topic["rank"] = idx + 1
        topic["previous_rank"] = topic.get("rank", idx + 1)

    return {
        "summary": {
            "total_topics": len(topics),
            "selected_count": len(reranked_topics),
            "rejected_count": len(rejected_topics),
            "top_score": reranked_topics[0]["final_score"] if reranked_topics else 0,
            "bottom_score": reranked_topics[-1]["final_score"] if reranked_topics else 0,
        },
        "reranked_topics": reranked_topics,
        "rejected_topics": rejected_topics,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Rerank main topic selection")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "config" / "topic_diversity_policy.yaml", help="Path to config file")
    parser.add_argument("--penalty", type=Path, default=OUTPUT_DIR / "latest_competitive_coverage_penalty.json", help="Path to penalty results")
    parser.add_argument("--boost", type=Path, default=OUTPUT_DIR / "latest_differentiated_angle_boost.json", help="Path to boost results")
    parser.add_argument("--guard", type=Path, default=OUTPUT_DIR / "latest_topic_title_normalization_guard.json", help="Path to guard results")
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

    penalty_results = []
    if args.penalty.exists():
        try:
            penalty_data = load_json(args.penalty)
            penalty_results = penalty_data.get("penalty_results", [])
        except Exception:
            pass

    boost_results = []
    if args.boost.exists():
        try:
            boost_data = load_json(args.boost)
            boost_results = boost_data.get("boost_results", [])
        except Exception:
            pass

    guard_results = []
    if args.guard.exists():
        try:
            guard_data = load_json(args.guard)
            guard_results = guard_data.get("guard_results", [])
        except Exception:
            pass

    rerank_data = rerank_topics(topics, penalty_results, boost_results, guard_results)

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "status": "SUCCESS",
        "dry_run": args.dry_run,
        **rerank_data,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_main_topic_selection_rerank.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_main_topic_selection_rerank.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())