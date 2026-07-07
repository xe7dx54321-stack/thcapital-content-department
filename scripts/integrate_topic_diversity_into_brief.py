#!/usr/bin/env python3
"""Integrate topic diversity data into brief generation."""

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


def integrate_diversity_into_brief(
    topics: list,
    penalty_results: list,
    boost_results: list,
    similarity_results: list,
    diversity_results: list,
    guard_results: list,
) -> dict:
    penalty_map = {r["topic_id"]: r for r in penalty_results}
    boost_map = {r["topic_id"]: r for r in boost_results}
    similarity_map = {r["topic_id"]: r for r in similarity_results}
    diversity_score_map = {r["topic_id"]: r for r in diversity_results}
    guard_map = {r["topic_id"]: r for r in guard_results}

    brief_integrations = []

    for topic in topics:
        topic_id = topic.get("topic_id", "")
        title = topic.get("title", "")

        penalty_result = penalty_map.get(topic_id, {})
        boost_result = boost_map.get(topic_id, {})
        similarity_result = similarity_map.get(topic_id, {})
        diversity_score = diversity_score_map.get(topic_id, {})
        guard_result = guard_map.get(topic_id, {})

        diversity_context = {
            "is_duplicate": similarity_result.get("is_duplicate", False),
            "most_similar_topic": similarity_result.get("most_similar_topic"),
            "source_repetition_penalty": penalty_result.get("source_repetition_penalty", 0),
            "lane_repetition_penalty": penalty_result.get("lane_repetition_penalty", 0),
            "source": diversity_score.get("source", ""),
            "lane": diversity_score.get("lane", ""),
            "source_count": diversity_score.get("source_count", 1),
            "lane_count": diversity_score.get("lane_count", 1),
            "penalties_applied": penalty_result.get("penalties", []),
            "boosts_applied": boost_result.get("boosts", []),
        }

        differentiated_angle = boost_result.get("angle_info", {})
        if differentiated_angle:
            diversity_context["differentiated_angle"] = {
                "type": differentiated_angle.get("type", ""),
                "confidence": differentiated_angle.get("confidence", 0),
                "description": differentiated_angle.get("description", ""),
            }

        normalized_title = guard_result.get("normalized_title", title)
        guard_issues = guard_result.get("issues", [])
        rejected_issues = [i for i in guard_issues if i.get("severity") == "REJECT"]

        brief_entry = {
            "topic_id": topic_id,
            "title": title,
            "normalized_title": normalized_title,
            "final_score": topic.get("final_score", topic.get("score", 0)),
            "is_rejected": len(rejected_issues) > 0,
            "rejection_reasons": rejected_issues,
            "diversity_context": diversity_context,
            "writing_guidance": generate_writing_guidance(diversity_context, guard_issues),
            "metadata": topic.get("metadata", {}),
        }

        brief_integrations.append(brief_entry)

    return {
        "summary": {
            "total_topics": len(topics),
            "integrated_count": len(brief_integrations),
            "rejected_count": len([b for b in brief_integrations if b["is_rejected"]]),
        },
        "brief_integrations": brief_integrations,
    }


def generate_writing_guidance(diversity_context: dict, guard_issues: list) -> dict:
    guidance = {
        "focus_points": [],
        "avoid_points": [],
        "angle_suggestions": [],
    }

    if diversity_context.get("is_duplicate"):
        guidance["focus_points"].append("需要提供新的角度或深度分析")
        guidance["avoid_points"].append("避免重复已有内容")
        similar_topic = diversity_context.get("most_similar_topic", {})
        if similar_topic:
            guidance["avoid_points"].append(f"避免与'{similar_topic.get('title', '')}'重复")

    if diversity_context.get("source_repetition_penalty", 0) > 0:
        guidance["focus_points"].append("寻找多个来源交叉验证")
        guidance["avoid_points"].append("避免单一来源依赖")

    if diversity_context.get("lane_repetition_penalty", 0) > 0:
        guidance["focus_points"].append("探索跨领域视角")

    differentiated_angle = diversity_context.get("differentiated_angle")
    if differentiated_angle:
        angle_type = differentiated_angle.get("type", "")
        guidance["angle_suggestions"].append(f"采用{angle_type}角度")
        guidance["focus_points"].append(f"深入分析{angle_type}方面")

    for issue in guard_issues:
        if issue.get("type") == "metadata_title":
            guidance["focus_points"].append("需要重写标题，使其更具可读性")
        elif issue.get("type") == "not_human_readable":
            guidance["focus_points"].append("优化标题表达，提高可读性")
        elif issue.get("type") == "missing_angle_for_repeated_event":
            guidance["focus_points"].append("为重复事件寻找差异化角度")

    return guidance


def main() -> int:
    parser = argparse.ArgumentParser(description="Integrate topic diversity into brief")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "config" / "topic_diversity_policy.yaml", help="Path to config file")
    parser.add_argument("--penalty", type=Path, default=OUTPUT_DIR / "latest_competitive_coverage_penalty.json", help="Path to penalty results")
    parser.add_argument("--boost", type=Path, default=OUTPUT_DIR / "latest_differentiated_angle_boost.json", help="Path to boost results")
    parser.add_argument("--similarity", type=Path, default=OUTPUT_DIR / "latest_topic_similarity_report.json", help="Path to similarity results")
    parser.add_argument("--diversity", type=Path, default=OUTPUT_DIR / "latest_source_lane_diversity.json", help="Path to diversity results")
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

    similarity_results = []
    if args.similarity.exists():
        try:
            similarity_data = load_json(args.similarity)
            similarity_results = similarity_data.get("similarity_scores", [])
        except Exception:
            pass

    diversity_results = []
    if args.diversity.exists():
        try:
            diversity_data = load_json(args.diversity)
            diversity_results = diversity_data.get("topic_diversity_scores", [])
        except Exception:
            pass

    guard_results = []
    if args.guard.exists():
        try:
            guard_data = load_json(args.guard)
            guard_results = guard_data.get("guard_results", [])
        except Exception:
            pass

    integration_data = integrate_diversity_into_brief(
        topics, penalty_results, boost_results, similarity_results, diversity_results, guard_results
    )

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "status": "SUCCESS",
        "dry_run": args.dry_run,
        **integration_data,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_topic_diversity_brief_integration.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_topic_diversity_brief_integration.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())