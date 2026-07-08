#!/usr/bin/env python3
"""
P36-004: Build Real Data Calibration Checklist
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.real_data_calibration_checklist import (
    build_real_data_calibration_checklist,
    save_calibration_checklist
)


def main():
    output_dir = get_project_paths(ROOT).logs_root
    
    result = build_real_data_calibration_checklist()
    outputs = save_calibration_checklist(result, output_dir)
    
    print("Real Data Calibration Checklist")
    print("=" * 40)
    print(f"checklist_count: {result.checklist_count}")
    print(f"rss_items: {len(result.rss_items)}")
    print(f"topic_items: {len(result.topic_items)}")
    print(f"editorial_items: {len(result.editorial_items)}")
    print(f"workbench_items: {len(result.workbench_items)}")
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