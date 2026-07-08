#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from content_system.phase35_editorial_quality_pipeline import run_phase35_pipeline
import json
import argparse


def main():
    parser = argparse.ArgumentParser(description="Run Phase35 Editorial Quality Pipeline")
    parser.add_argument("--topic-id", default="topic_001", help="Topic ID")
    parser.add_argument("--topic-title", default="AI芯片市场格局变化", help="Topic title")
    parser.add_argument("--topic-type", default="news_event", help="Topic type")
    parser.add_argument("--angle-type", default="产业影响", help="Angle type")
    parser.add_argument("--draft-text", default="AI芯片市场正在发生深刻变化。NVIDIA发布了新的GPU产品，这对整个AI芯片产业产生了重大影响。", help="Draft text for style quality scoring")
    parser.add_argument("--draft-file", help="Draft file path for style quality scoring")
    parser.add_argument("--original-version", default="AI芯片市场正在发生深刻变化。值得关注的是，这一趋势未来可期。", help="Original version text for comparison")
    parser.add_argument("--new-version", default="AI芯片市场正在发生深刻变化。根据最新数据，NVIDIA发布新GPU，我们认为这重新定义了AI芯片竞争格局，关键在于其性能提升幅度超过市场预期。这对投资者意味着实际的配置调整机会，但需要注意供应链风险。", help="New version text for comparison")
    parser.add_argument("--dry-run", action="store_true", help="Run pipeline without writing output files")
    parser.add_argument("--json", action="store_true", help="Print JSON pipeline report to stdout")
    parser.add_argument("--continue-on-error", action="store_true", help="Attempt downstream steps after a failed step")
    args = parser.parse_args()

    if args.draft_file and os.path.exists(args.draft_file):
        with open(args.draft_file, "r", encoding="utf-8") as f:
            args.draft_text = f.read()

    result = run_phase35_pipeline(
        topic_id=args.topic_id,
        topic_title=args.topic_title,
        topic_type=args.topic_type,
        angle_type=args.angle_type,
        draft_text=args.draft_text,
        original_version=args.original_version,
        new_version=args.new_version,
    )

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
        return 0

    print("Phase35 Editorial Quality Pipeline")
    print("==================================")
    print(f"status: {result.status}")
    print(f"run_date: {result.run_date}")
    print(f"style_guide_valid: {result.style_guide_valid}")
    print(f"frameworks_valid: {result.frameworks_valid}")
    print(f"framework_count: {result.framework_count}")
    print(f"title_candidate_count: {result.title_candidate_count}")
    print(f"compliant_title_count: {result.compliant_title_count}")
    print(f"ai_taste_passed: {result.ai_taste_passed}")
    print(f"draft_style_score: {result.draft_style_score}")
    print(f"draft_style_grade: {result.draft_style_grade}")
    print(f"version_gate_decision: {result.version_gate_decision}")

    print("\nSteps:")
    for step in result.steps:
        status_icon = "OK" if step.status == "OK" else "FAILED"
        print(f"  {step.name}: {status_icon} ({step.returncode})")

    print("\nPipeline Outputs:")
    dated_json = os.path.join("同行资本市场内容系统/10_logs", f"{result.run_date}__phase35-editorial-quality-pipeline.json")
    latest_json = os.path.join("同行资本市场内容系统/10_logs", "latest_phase35_editorial_quality_pipeline.json")
    print(f"  dated_json: {dated_json}")
    print(f"  latest_json: {latest_json}")

    return 0 if result.status == "SUCCESS" else 1


if __name__ == "__main__":
    sys.exit(main())
