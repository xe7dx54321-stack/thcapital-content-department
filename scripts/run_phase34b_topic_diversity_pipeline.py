#!/usr/bin/env python3
"""Run Phase 34B Topic Diversity Pipeline."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "ignored"
SCRIPTS_DIR = REPO_ROOT / "scripts"


def run_script(script_name: str, dry_run: bool) -> tuple[int, str]:
    script_path = SCRIPTS_DIR / script_name
    cmd = ["python", str(script_path)]
    if dry_run:
        cmd.append("--dry-run")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO_ROOT)
        return result.returncode, result.stdout
    except Exception as e:
        return 1, str(e)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Phase 34B Topic Diversity Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument("--output", type=Path, default=None, help="Output JSON file path")
    args = parser.parse_args()

    pipeline_steps = [
        ("build_topic_history_memory.py", "构建topic历史记忆"),
        ("score_topic_similarity.py", "计算topic相似度"),
        ("score_source_lane_diversity.py", "计算source/lane多样性"),
        ("apply_competitive_coverage_penalty.py", "应用竞品覆盖惩罚"),
        ("apply_differentiated_angle_boost.py", "应用差异化角度增强"),
        ("run_topic_title_normalization_guard.py", "运行标题规范化guard"),
        ("rerank_main_topic_selection.py", "主选题二次排序"),
        ("integrate_topic_diversity_into_brief.py", "整合到brief"),
    ]

    step_results = []
    overall_status = "SUCCESS"
    failed_steps = []

    for script_name, description in pipeline_steps:
        print(f"Running: {description} ({script_name})")
        returncode, output = run_script(script_name, args.dry_run)
        status = "SUCCESS" if returncode == 0 else "FAILED"
        if status == "FAILED":
            overall_status = "FAILED"
            failed_steps.append(description)

        step_results.append({
            "step": description,
            "script": script_name,
            "status": status,
            "returncode": returncode,
        })
        print(f"  Status: {status}")

    result = {
        "schema_version": "v1",
        "generated_at": datetime.now().isoformat(),
        "pipeline": "phase34b_topic_diversity",
        "status": overall_status,
        "dry_run": args.dry_run,
        "total_steps": len(pipeline_steps),
        "success_steps": len([s for s in step_results if s["status"] == "SUCCESS"]),
        "failed_steps": len(failed_steps),
        "failed_steps_list": failed_steps,
        "steps": step_results,
        "output_files": [
            "latest_topic_history_memory.json",
            "latest_topic_similarity_report.json",
            "latest_source_lane_diversity.json",
            "latest_competitive_coverage_penalty.json",
            "latest_differentiated_angle_boost.json",
            "latest_topic_title_normalization_guard.json",
            "latest_main_topic_selection_rerank.json",
            "latest_topic_diversity_brief_integration.json",
        ],
    }

    print("\n" + "=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_phase34b_topic_diversity_pipeline.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_phase34b_topic_diversity_pipeline.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0 if overall_status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())