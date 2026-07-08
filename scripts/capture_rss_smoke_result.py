#!/usr/bin/env python3
"""P37A-002: RSS Smoke Result Capture"""
import sys
sys.path.insert(0, '/workspace/src')
from pathlib import Path
from content_system.rss_smoke_result_capture import (
    build_rss_smoke_result,
    save_rss_smoke_result
)

def main():
    output_dir = Path("/workspace/同行资本市场内容系统/10_logs")
    result = build_rss_smoke_result(cloud_mode=True)
    outputs = save_rss_smoke_result(result, output_dir)
    
    print("RSS Smoke Result Capture")
    print("=" * 40)
    print(f"status: {result.status}")
    print(f"requires_real_rss: {result.requires_real_rss}")
    print(f"blocking_failures: {result.blocking_failures}")
    print()
    print("Output files:")
    print(f"  dated_json: {outputs['dated_json']}")
    print(f"  latest_json: {outputs['latest_json']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())