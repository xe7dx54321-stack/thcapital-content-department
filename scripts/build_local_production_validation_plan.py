#!/usr/bin/env python3
"""
P36-001: Build Local Production Validation Plan
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from content_system.paths import get_project_paths
from content_system.local_production_validation import (
    build_local_production_validation_plan,
    save_validation_plan
)


def main():
    output_dir = get_project_paths(ROOT).logs_root
    
    result = build_local_production_validation_plan()
    outputs = save_validation_plan(result, output_dir)
    
    print("Local Production Validation Plan")
    print("=" * 40)
    print(f"status: {result.status}")
    print(f"checklist_count: {result.checklist_count}")
    print(f"local_only_items: {result.local_only_items}")
    print(f"cloud_safe_items: {result.cloud_safe_items}")
    print()
    print("Output files:")
    print(f"  dated_json: {outputs['dated_json']}")
    print(f"  latest_json: {outputs['latest_json']}")
    print(f"  dated_md: {outputs['dated_md']}")
    print(f"  latest_md: {outputs['latest_md']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())