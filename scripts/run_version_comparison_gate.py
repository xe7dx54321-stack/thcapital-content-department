#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from content_system.version_comparison_gate import compare_versions
import json
from datetime import datetime
import argparse


def main():
    parser = argparse.ArgumentParser(description="Run version comparison gate")
    parser.add_argument("--original-text", default="AI芯片市场正在发生深刻变化。值得关注的是，这一趋势未来可期。", help="Original text")
    parser.add_argument("--new-text", default="AI芯片市场正在发生深刻变化。根据最新数据，NVIDIA发布新GPU，我们认为这重新定义了AI芯片竞争格局，关键在于其性能提升幅度超过市场预期。这对投资者意味着实际的配置调整机会，但需要注意供应链风险。", help="New text")
    args = parser.parse_args()

    result = compare_versions(
        original_text=args.original_text,
        rewritten_text=args.new_text,
    )

    print("Version Comparison Gate")
    print("=======================")
    print(f"overall_decision: {'accept' if result.accept_rewrite else 'reject'}")
    print(f"improvement_score: {result.improvement_score}")
    print(f"min_improvement_required: 0.05")

    print("\nMetrics Comparison:")
    for metric in result.metric_comparisons:
        trend = "↑" if metric.delta > 0 else ("↓" if metric.delta < 0 else "→")
        print(f"  {metric.metric_id}: {metric.original_score} → {metric.rewritten_score} ({trend} {abs(metric.delta)})")

    print("\nRegression Checks:")
    if result.regressions:
        for reg in result.regressions:
            print(f"  ✗ {reg}")
    else:
        print(f"  ✓ No regressions")

    print(f"\nApplied Rules:")
    print(f"  - {result.reason}")

    print("\nSummary:")
    print(f"  improvement_score: {result.improvement_score}")
    print(f"  any_regression: {len(result.regressions) > 0}")
    print(f"  accept_rewrite: {result.accept_rewrite}")

    run_date = datetime.now().strftime("%Y%m%d")
    logs_root = "同行资本市场内容系统/10_logs"
    os.makedirs(logs_root, exist_ok=True)

    dated_path = os.path.join(logs_root, f"{run_date}__version-comparison-gate.json")
    latest_path = os.path.join(logs_root, "latest_version_comparison_gate.json")

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
