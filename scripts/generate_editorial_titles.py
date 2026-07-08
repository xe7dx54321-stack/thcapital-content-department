#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from content_system.title_generator import generate_title_candidates
import json
from datetime import datetime
import argparse


def main():
    parser = argparse.ArgumentParser(description="Generate editorial title candidates")
    parser.add_argument("--topic-title", default="AI芯片市场格局变化", help="Topic title")
    args = parser.parse_args()

    result = generate_title_candidates(topic_title=args.topic_title)

    print("Editorial Title Generation")
    print("==========================")
    print(f"candidate_count: {len(result.candidates)}")
    print(f"compliant_count: {result.compliant_count}")
    print(f"recommended_count: {result.recommended_count}")
    print(f"forbidden_hit_count: {result.forbidden_hit_count}")

    print("\nCandidates:")
    for i, candidate in enumerate(result.candidates):
        status = "✓" if candidate.recommended else "✗"
        print(f"  {status} [{candidate.angle_variant}] {candidate.title}")
        print(f"     score: {candidate.score}, forbidden: {candidate.forbidden_pattern_hit}")

    run_date = datetime.now().strftime("%Y%m%d")
    logs_root = "同行资本市场内容系统/10_logs"
    os.makedirs(logs_root, exist_ok=True)

    dated_path = os.path.join(logs_root, f"{run_date}__editorial-title-candidates.json")
    latest_path = os.path.join(logs_root, "latest_editorial_title_candidates.json")

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
