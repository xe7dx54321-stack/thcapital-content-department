#!/usr/bin/env python3
"""P37A-004: Build Manual Observation Log"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.manual_observation_log import (
    build_manual_observation_log,
    save_manual_observation_log
)

def main():
    output_dir = get_project_paths(ROOT).logs_root
    result = build_manual_observation_log(day_slots=2)
    outputs = save_manual_observation_log(result, output_dir)
    
    print("Manual Observation Log")
    print("=" * 40)
    print(f"day_slots: {result.day_slots}")
    print(f"checklist_count: {result.checklist_count}")
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