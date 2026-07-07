#!/usr/bin/env python3
"""Run Phase 34A WeChat RSS Intelligence Pipeline."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = REPO_ROOT / "同行资本市场内容系统" / "10_logs"
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
    parser = argparse.ArgumentParser(description="Run Phase 34A WeChat RSS Intelligence Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    parser.add_argument("--output", type=Path, default=None, help="Output JSON file path")
    args = parser.parse_args()

    pipeline_steps = [
        ("validate_wechat_rss_sources.py", "验证RSS源配置"),
        ("run_wechat_rss_ingestion.py", "运行RSS抓取"),
        ("clean_wechat_rss_articles.py", "运行清洗和去重"),
        ("extract_wechat_article_intelligence.py", "运行情报抽取"),
        ("run_competitive_coverage_analysis.py", "运行竞品覆盖分析"),
        ("recommend_differentiated_angles.py", "运行差异化角度推荐"),
        ("check_wechat_evidence_support.py", "运行证据支持检查"),
        ("extract_wechat_style_patterns.py", "运行风格pattern抽取"),
        ("run_wechat_intelligence_integration.py", "运行集成"),
        ("run_wechat_rss_usage_boundary_gate.py", "运行边界检查"),
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
        "pipeline": "phase34a_wechat_rss_intelligence",
        "status": overall_status,
        "dry_run": args.dry_run,
        "total_steps": len(pipeline_steps),
        "success_steps": len([s for s in step_results if s["status"] == "SUCCESS"]),
        "failed_steps": len(failed_steps),
        "failed_steps_list": failed_steps,
        "steps": step_results,
    }

    print("\n" + "=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not args.dry_run:
        if args.output:
            output_path = args.output
        else:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = OUTPUT_DIR / f"{timestamp}_phase34a_pipeline.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        latest_path = OUTPUT_DIR / "latest_phase34a_pipeline.json"
        with open(latest_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return 0 if overall_status == "SUCCESS" else 1


if __name__ == "__main__":
    raise SystemExit(main())