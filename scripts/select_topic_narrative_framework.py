#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from content_system.topic_framework_selector import select_topic_framework
import json
from datetime import datetime
import argparse


def main():
    parser = argparse.ArgumentParser(description="Select narrative framework for a topic")
    parser.add_argument("--topic-id", default="topic_001", help="Topic ID")
    parser.add_argument("--topic-type", default="news_event", help="Topic type")
    parser.add_argument("--event-type", help="Event type")
    parser.add_argument("--angle-type", default="产业影响", help="Angle type")
    parser.add_argument("--differentiated-angle", help="Differentiated angle description")
    parser.add_argument("--evidence-strength", type=float, default=0.5, help="Evidence strength (0-1)")
    args = parser.parse_args()

    result = select_topic_framework(
        topic_id=args.topic_id,
        topic_type=args.topic_type,
        event_type=args.event_type,
        angle_type=args.angle_type,
        differentiated_angle=args.differentiated_angle,
        evidence_strength=args.evidence_strength,
    )

    print("Topic Framework Selection")
    print("=========================")
    print(f"topic_id: {result.topic_id}")
    print(f"selected_framework: {result.selected_framework.name if result.selected_framework else 'None'}")
    print(f"reason: {result.reason}")
    print(f"confidence: {result.confidence}")
    print(f"fallback_used: {result.fallback_used}")

    run_date = datetime.now().strftime("%Y%m%d")
    logs_root = "同行资本市场内容系统/10_logs"
    os.makedirs(logs_root, exist_ok=True)

    dated_path = os.path.join(logs_root, f"{run_date}__topic-framework-selection.json")
    latest_path = os.path.join(logs_root, "latest_topic_framework_selection.json")

    with open(dated_path, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)

    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)

    print(f"\nOutput files:")
    print(f"  dated_json: {dated_path}")
    print(f"  latest_json: {latest_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
