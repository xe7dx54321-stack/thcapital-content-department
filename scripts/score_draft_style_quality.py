#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from content_system.draft_style_quality_scorer import score_draft_quality
import json
from datetime import datetime
import argparse


def main():
    parser = argparse.ArgumentParser(description="Score draft style quality")
    parser.add_argument("--draft-text", default="AI芯片市场正在发生深刻变化。NVIDIA发布了新的GPU产品，这对整个AI芯片产业产生了重大影响。", help="Draft text")
    parser.add_argument("--title", default="", help="Article title")
    args = parser.parse_args()

    result = score_draft_quality(draft_text=args.draft_text, title=args.title)

    print("Draft Style Quality Score")
    print("=========================")
    print(f"overall_style_score: {result.overall_style_score}")
    print(f"grade: {result.grade}")
    print(f"blocking_issues_count: {len(result.blocking_issues)}")
    print(f"revision_suggestions_count: {len(result.revision_suggestions)}")

    print("\nDimension Scores:")
    for dim in result.dimension_scores:
        print(f"  {dim.dimension}: {dim.score} (weight: {dim.weight})")

    print("\nBlocking Issues:")
    for issue in result.blocking_issues:
        print(f"  - {issue}")

    print("\nRevision Suggestions:")
    for suggestion in result.revision_suggestions:
        print(f"  - {suggestion}")

    run_date = datetime.now().strftime("%Y%m%d")
    logs_root = "同行资本市场内容系统/10_logs"
    os.makedirs(logs_root, exist_ok=True)

    dated_path = os.path.join(logs_root, f"{run_date}__draft-style-quality-score.json")
    latest_path = os.path.join(logs_root, "latest_draft_style_quality_score.json")

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
