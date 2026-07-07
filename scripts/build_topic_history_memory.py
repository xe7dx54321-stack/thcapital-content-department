#!/usr/bin/env python3
"""Build topic history memory for diversity analysis."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "ignored"
TOPIC_RADAR_DIR = REPO_ROOT / "同行资本市场内容系统" / "02_topic_radar"
REPLAY_DIR = REPO_ROOT / "同行资本市场内容系统" / "13_replay"


def load_config(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def collect_historical_topics(config: dict, dry_run: bool) -> dict:
    history_window_days = config.get("history_window_days", 7)
    cutoff_date = datetime.now() - timedelta(days=history_window_days)

    historical_topics = []
    source_counts = {}
    lane_counts = {}
    topic_by_date = {}

    if not dry_run:
        for replay_dir in REPLAY_DIR.iterdir():
            if not replay_dir.is_dir():
                continue
            if not replay_dir.name.startswith("replay_"):
                continue

            date_str = replay_dir.name.replace("replay_", "")
            try:
                replay_date = datetime.strptime(date_str, "%Y%m%d")
            except ValueError:
                continue

            if replay_date < cutoff_date:
                continue

            main_topic_file = replay_dir / "main_topic_selection.json"
            if main_topic_file.exists():
                try:
                    with open(main_topic_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    if "selected_topics" in data:
                        for topic in data["selected_topics"]:
                            historical_topics.append({
                                "topic_id": topic.get("topic_id", ""),
                                "title": topic.get("title", ""),
                                "normalized_title": topic.get("normalized_title", ""),
                                "source": topic.get("source", ""),
                                "lane": topic.get("lane", ""),
                                "date": date_str,
                                "score": topic.get("score", 0),
                                "entities": topic.get("entities", []),
                                "companies": topic.get("companies", []),
                                "event_type": topic.get("event_type", ""),
                            })
                            source = topic.get("source", "unknown")
                            lane = topic.get("lane", "unknown")
                            source_counts[source] = source_counts.get(source, 0) + 1
                            lane_counts[lane] = lane_counts.get(lane, 0) + 1
                            if date_str not in topic_by_date:
                                topic_by_date[date_str] = []
                            topic_by_date[date_str].append(topic.get("title", ""))
                except Exception:
                    pass

        asset_chains_dir = TOPIC_RADAR_DIR / "asset_chains"
        if asset_chains_dir.exists():
            for asset_file in asset_chains_dir.iterdir():
                if not asset_file.is_file() or not asset_file.name.endswith(".json"):
                    continue

                date_str = asset_file.name[:8]
                try:
                    asset_date = datetime.strptime(date_str, "%Y%m%d")
                except ValueError:
                    continue

                if asset_date < cutoff_date:
                    continue

                try:
                    with open(asset_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    historical_topics.append({
                        "topic_id": data.get("id", ""),
                        "title": data.get("title", ""),
                        "normalized_title": data.get("normalized_title", ""),
                        "source": data.get("source", "unknown"),
                        "lane": data.get("lane", "unknown"),
                        "date": date_str,
                        "score": data.get("score", 0),
                        "entities": data.get("entities", []),
                        "companies": data.get("companies", []),
                        "event_type": data.get("event_type", ""),
                    })
                except Exception:
                    pass

    return {
        "history_window_days": history_window_days,
        "cutoff_date": cutoff_date.isoformat(),
        "total_topics": len(historical_topics),
        "unique_sources": len(source_counts),
        "unique_lanes": len(lane_counts),
        "source_distribution": source_counts,
        "lane_distribution": lane_counts,
        "topics_by_date": topic_by_date,
        "topics": historical_topics,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build topic history memory")
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "config" / "topic_diversity_policy.yaml", help="Path to config file")
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

    history_data = collect_historical_topics(config, args.dry_run)

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "status": "SUCCESS",
        "dry_run": args.dry_run,
        "policy_config": {
            "history_window_days": config.get("history_window_days", 7),
            "duplicate_similarity_threshold": config.get("duplicate_similarity_threshold", 0.72),
            "hard_duplicate_threshold": config.get("hard_duplicate_threshold", 0.88),
        },
        "data": history_data,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_topic_history_memory.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_topic_history_memory.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())