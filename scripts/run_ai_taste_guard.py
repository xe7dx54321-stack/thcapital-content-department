#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from content_system.ai_taste_guard import detect_ai_taste, get_ai_taste_rule_count
import json
from datetime import datetime
import argparse


def main():
    parser = argparse.ArgumentParser(description="Run AI taste guard check")
    parser.add_argument("--text", default="AI芯片市场正在发生深刻变化。值得关注的是，这一趋势未来可期。", help="Text to check")
    args = parser.parse_args()

    result = detect_ai_taste(args.text)
    rule_count = get_ai_taste_rule_count()

    print("AI Taste Guard")
    print("==============")
    print(f"rule_count: {rule_count}")
    print(f"hit_count: {result.hit_count}")
    print(f"high_severity_count: {result.high_severity_count}")
    print(f"ai_taste_score: {result.ai_taste_score}")

    print("\nViolations:")
    for violation in result.violations:
        print(f"  [{violation.severity}] '{violation.phrase}' ({violation.category})")
        print(f"     suggestion: {violation.suggestion}")
        print(f"     paragraph_id: {violation.paragraph_id}")

    run_date = datetime.now().strftime("%Y%m%d")
    logs_root = "同行资本市场内容系统/10_logs"
    os.makedirs(logs_root, exist_ok=True)

    dated_path = os.path.join(logs_root, f"{run_date}__ai-taste-guard.json")
    latest_path = os.path.join(logs_root, "latest_ai_taste_guard.json")

    output = {
        "rule_count": rule_count,
        "detection": result.to_dict(),
    }

    with open(dated_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nOutput files:")
    print(f"  dated_json: {dated_path}")
    print(f"  latest_json: {latest_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
