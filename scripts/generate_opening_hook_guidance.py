#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from content_system.opening_hook_guidance import generate_opening_hook, check_marketing_style
import json
from datetime import datetime
import argparse


def main():
    parser = argparse.ArgumentParser(description="Generate opening hook guidance")
    parser.add_argument("--topic-title", default="AI芯片市场格局变化", help="Topic title")
    parser.add_argument("--framework-name", help="Narrative framework name")
    args = parser.parse_args()

    guidance = generate_opening_hook(
        topic_title=args.topic_title,
        framework_name=args.framework_name,
    )

    print("Opening Hook Guidance")
    print("=====================")
    print(f"hook_strategy: {guidance.hook_strategy}")
    print(f"opening_question: {guidance.opening_question}")
    print(f"first_paragraph_guidance: {guidance.first_paragraph_guidance}")
    print(f"avoid_opening_patterns: {', '.join(guidance.avoid_opening_patterns[:5])}...")

    sample_opening = f"震惊！{args.topic_title}背后的真相竟然是..."
    marketing_check = check_marketing_style(sample_opening)
    print(f"\nMarketing style check (sample):")
    print(f"  has_marketing_style: {marketing_check['has_marketing_style']}")
    print(f"  suggestion: {marketing_check['suggestion']}")

    run_date = datetime.now().strftime("%Y%m%d")
    logs_root = "同行资本市场内容系统/10_logs"
    os.makedirs(logs_root, exist_ok=True)

    dated_path = os.path.join(logs_root, f"{run_date}__opening-hook-guidance.json")
    latest_path = os.path.join(logs_root, "latest_opening_hook_guidance.json")

    output = {
        "guidance": guidance.to_dict(),
        "marketing_style_check_example": marketing_check,
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
