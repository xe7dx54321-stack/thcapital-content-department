#!/usr/bin/env python3
"""P37A-001: Build Production Observation Schema"""
import sys
sys.path.insert(0, '/workspace/src')
from pathlib import Path
from content_system.production_observation_result import (
    build_production_observation_schema,
    save_observation_schema
)

def main():
    output_dir = Path("/workspace/同行资本市场内容系统/10_logs")
    result = build_production_observation_schema(mode="CLOUD_DEVELOPMENT")
    outputs = save_observation_schema(result, output_dir)
    
    print("Production Observation Schema")
    print("=" * 40)
    print(f"mode: {result.mode}")
    print(f"status: {result.status}")
    print(f"section_count: {result.section_count}")
    print(f"next_action: {result.next_action}")
    print()
    print("Output files:")
    print(f"  dated_json: {outputs['dated_json']}")
    print(f"  latest_json: {outputs['latest_json']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())