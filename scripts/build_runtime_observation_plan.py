#!/usr/bin/env python3
"""
P36-003: Build Runtime Observation Plan
"""

import sys
sys.path.insert(0, '/workspace/src')

from pathlib import Path
from content_system.runtime_observation_plan import (
    build_runtime_observation_plan,
    save_runtime_observation_plan
)


def main():
    output_dir = Path("/workspace/同行资本市场内容系统/10_logs")
    
    result = build_runtime_observation_plan()
    outputs = save_runtime_observation_plan(result, output_dir)
    
    print("Runtime Observation Plan")
    print("=" * 40)
    print(f"requires_mac_runtime: {result.requires_mac_runtime}")
    print(f"observation_days: {result.observation_days}")
    print(f"step_count: {result.step_count}")
    print(f"status: {result.status}")
    print()
    print("Output files:")
    print(f"  dated_json: {outputs['dated_json']}")
    print(f"  latest_json: {outputs['latest_json']}")
    print(f"  dated_md: {outputs['dated_md']}")
    print(f"  latest_md: {outputs['latest_md']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())