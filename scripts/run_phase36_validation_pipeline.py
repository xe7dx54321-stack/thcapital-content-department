#!/usr/bin/env python3
"""
P36-007: Run Phase36 Validation Pipeline
"""

import sys
sys.path.insert(0, '/workspace/src')

from pathlib import Path
from content_system.phase36_validation_pipeline import (
    run_phase36_validation_pipeline,
    save_pipeline_result
)


def main():
    output_dir = Path("/workspace/同行资本市场内容系统/10_logs")
    
    result = run_phase36_validation_pipeline(dry_run=True)
    outputs = save_pipeline_result(result, output_dir)
    
    print("Phase36 Validation Pipeline")
    print("=" * 40)
    print(f"overall_status: {result.overall_status}")
    print(f"total_steps: {result.total_steps}")
    print(f"success_steps: {result.success_steps}")
    print(f"failed_steps: {result.failed_steps}")
    print(f"dry_run: {result.dry_run}")
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