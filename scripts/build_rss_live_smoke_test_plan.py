#!/usr/bin/env python3
"""
P36-002: Build RSS Live Smoke Test Plan
"""

import sys
sys.path.insert(0, '/workspace/src')

from pathlib import Path
from content_system.rss_live_smoke_plan import (
    build_rss_live_smoke_plan,
    save_smoke_test_plan
)


def main():
    output_dir = Path("/workspace/同行资本市场内容系统/10_logs")
    
    result = build_rss_live_smoke_plan()
    outputs = save_smoke_test_plan(result, output_dir)
    
    print("RSS Live Smoke Test Plan")
    print("=" * 40)
    print(f"enabled: {result.enabled}")
    print(f"requires_real_execution: {result.requires_real_execution}")
    print(f"max_sources: {result.max_sources}")
    print(f"max_articles_per_source: {result.max_articles_per_source}")
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