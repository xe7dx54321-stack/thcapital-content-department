#!/usr/bin/env python3
"""Score topic similarity against historical memory."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List

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


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def jaccard_similarity(a: str, b: str) -> float:
    a_tokens = set(normalize_text(a).split())
    b_tokens = set(normalize_text(b).split())
    if not a_tokens and not b_tokens:
        return 0.0
    intersection = len(a_tokens & b_tokens)
    union = len(a_tokens | b_tokens)
    return intersection / union if union > 0 else 0.0


def calculate_entity_overlap(entities_a: List[str], entities_b: List[str]) -> float:
    set_a = set(e.lower() for e in entities_a)
    set_b = set(e.lower() for e in entities_b)
    if not set_a and not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0


def score_topic_similarity(
    topic: dict,
    history_topics: List[dict],
    similarity_weights: dict,
    threshold: float,
) -> dict:
    similarities = []
    max_similarity = 0.0
    most_similar_topic = None

    for history_topic in history_topics:
        title_sim = jaccard_similarity(topic.get("title", ""), history_topic.get("title", ""))
        norm_title_sim = jaccard_similarity(
            topic.get("normalized_title", topic.get("title", "")),
            history_topic.get("normalized_title", history_topic.get("title", "")),
        )
        entity_overlap = calculate_entity_overlap(
            topic.get("entities", []), history_topic.get("entities", [])
        )
        company_overlap = calculate_entity_overlap(
            topic.get("companies", []), history_topic.get("companies", [])
        )
        event_type_match = 1.0 if topic.get("event_type") == history_topic.get("event_type") else 0.0

        weighted_sim = (
            title_sim * similarity_weights.get("title_similarity", 0.35)
            + norm_title_sim * similarity_weights.get("normalized_title_similarity", 0.25)
            + entity_overlap * similarity_weights.get("entity_overlap", 0.20)
            + company_overlap * similarity_weights.get("company_overlap", 0.10)
            + event_type_match * similarity_weights.get("event_type_match", 0.10)
        )

        similarities.append({
            "topic_id": history_topic.get("topic_id", ""),
            "title": history_topic.get("title", ""),
            "date": history_topic.get("date", ""),
            "similarity_score": weighted_sim,
            "breakdown": {
                "title_similarity": title_sim,
                "normalized_title_similarity": norm_title_sim,
                "entity_overlap": entity_overlap,
                "company_overlap": company_overlap,
                "event_type_match": event_type_match,
            },
        })

        if weighted_sim > max_similarity:
            max_similarity = weighted_sim
            most_similar_topic = history_topic

    is_duplicate = max_similarity >= threshold

    return {
        "topic_id": topic.get("topic_id", ""),
        "title": topic.get("title", ""),
        "max_similarity_score": max_similarity,
        "is_duplicate": is_duplicate,
        "most_similar_topic": {
            "topic_id": most_similar_topic.get("topic_id", "") if most_similar_topic else "",
            "title": most_similar_topic.get("title", "") if most_similar_topic else "",
            "date": most_similar_topic.get("date", "") if most_similar_topic else "",
        } if most_similar_topic else None,
        "similarity_details": sorted(similarities, key=lambda x: x["similarity_score"], reverse=True)[:5],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score topic similarity")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "config" / "topic_diversity_policy.yaml", help="Path to config file")
    parser.add_argument("--history", type=Path, default=OUTPUT_DIR / "latest_topic_history_memory.json", help="Path to history memory file")
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

    try:
        history_data = load_json(args.history)
        history_topics = history_data.get("data", {}).get("topics", [])
    except Exception:
        history_topics = []

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

    similarity_weights = config.get("similarity_weights", {})
    duplicate_threshold = config.get("duplicate_similarity_threshold", 0.72)

    similarity_scores = []
    duplicate_count = 0

    for topic in topics:
        score = score_topic_similarity(topic, history_topics, similarity_weights, duplicate_threshold)
        similarity_scores.append(score)
        if score["is_duplicate"]:
            duplicate_count += 1

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "status": "SUCCESS",
        "dry_run": args.dry_run,
        "policy_config": {
            "similarity_weights": similarity_weights,
            "duplicate_similarity_threshold": duplicate_threshold,
        },
        "summary": {
            "total_topics": len(topics),
            "duplicate_count": duplicate_count,
            "unique_count": len(topics) - duplicate_count,
        },
        "similarity_scores": similarity_scores,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_topic_similarity_report.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_topic_similarity_report.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())