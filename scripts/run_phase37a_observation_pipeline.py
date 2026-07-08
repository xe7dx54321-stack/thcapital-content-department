#!/usr/bin/env python3
"""P37A: Run Phase37A Observation Pipeline"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.phase37a_observation_pipeline import (
    run_phase37a_pipeline,
    save_pipeline_result
)

def main():
    output_dir = get_project_paths(ROOT).logs_root
    result = run_phase37a_pipeline(dry_run=True)
    outputs = save_pipeline_result(result, output_dir)
    
    print("Phase37A Observation Pipeline")
    print("=" * 40)
    print(f"overall_status: {result.overall_status}")
    print(f"total_steps: {result.total_steps}")
    print(f"success_steps: {result.success_steps}")
    print(f"failed_steps: {result.failed_steps}")
    print(f"cloud_mode: {result.cloud_mode}")
    print()
    print("Step Results:")
    for step in result.steps:
        print(f"  {step.step_id}: {step.status} ({step.returncode})")
    print()
    print("Output files:")
    print(f"  dated_json: {outputs['dated_json']}")
    print(f"  latest_json: {outputs['latest_json']}")
    
    if result.overall_status == "FAILURE":
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())