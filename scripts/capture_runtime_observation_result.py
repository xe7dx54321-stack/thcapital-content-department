#!/usr/bin/env python3
"""P37A-003: Runtime Observation Result Capture"""
import sys
sys.path.insert(0, '/workspace/src')
from pathlib import Path
from content_system.runtime_observation_result_capture import (
    build_runtime_observation_result,
    save_runtime_observation_result
)

def main():
    output_dir = Path("/workspace/同行资本市场内容系统/10_logs")
    result = build_runtime_observation_result(cloud_mode=True)
    outputs = save_runtime_observation_result(result, output_dir)
    
    print("Runtime Observation Result Capture")
    print("=" * 40)
    print(f"status: {result.status}")
    print(f"requires_mac_runtime: {result.requires_mac_runtime}")
    print(f"blocking_failures: {result.blocking_failures}")
    print(f"observation_days: {result.observation_days}")
    print()
    print("Output files:")
    print(f"  dated_json: {outputs['dated_json']}")
    print(f"  latest_json: {outputs['latest_json']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())