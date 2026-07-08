#!/usr/bin/env python3
"""P37A-005: Build Production Observation Dashboard"""
import sys
sys.path.insert(0, '/workspace/src')
from pathlib import Path
from content_system.production_observation_dashboard import (
    build_production_observation_dashboard,
    save_dashboard
)

def main():
    output_dir = Path("/workspace/同行资本市场内容系统/10_logs")
    result = build_production_observation_dashboard(mode="CLOUD_DEVELOPMENT")
    outputs = save_dashboard(result, output_dir)
    
    print("Production Observation Dashboard")
    print("=" * 40)
    print(f"mode: {result.mode}")
    print(f"readiness_status: {result.readiness_status}")
    print(f"rss_status: {result.rss_status}")
    print(f"runtime_status: {result.runtime_status}")
    print(f"blocking_issues: {len(result.blocking_issues)}")
    print(f"warning_issues: {len(result.warning_issues)}")
    print(f"next_action: {result.next_action}")
    print()
    print("Output files:")
    print(f"  dated_json: {outputs['dated_json']}")
    print(f"  latest_json: {outputs['latest_json']}")
    print(f"  dated_md: {outputs['dated_md']}")
    print(f"  latest_md: {outputs['latest_md']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())