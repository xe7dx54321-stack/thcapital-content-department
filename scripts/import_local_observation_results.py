#!/usr/bin/env python3
"""P37A-007: Import Local Observation Results"""
import sys
sys.path.insert(0, '/workspace/src')
from pathlib import Path
from content_system.local_result_importer import (
    import_local_results,
    save_import_summary
)

def main():
    output_dir = Path("/workspace/同行资本市场内容系统/10_logs")
    result = import_local_results(output_dir)
    outputs = save_import_summary(result, output_dir)
    
    print("Local Observation Result Import")
    print("=" * 40)
    print(f"status: {result.status}")
    print(f"local_result_count: {result.local_result_count}")
    print(f"missing_file_count: {result.missing_file_count}")
    print(f"rss_smoke_status: {result.rss_smoke_status}")
    print(f"runtime_observation_status: {result.runtime_observation_status}")
    print(f"blocking_failures: {result.blocking_failures}")
    print(f"recommended_next_action: {result.recommended_next_action}")
    print()
    print("Output files:")
    print(f"  dated_json: {outputs['dated_json']}")
    print(f"  latest_json: {outputs['latest_json']}")
    print(f"  dated_md: {outputs['dated_md']}")
    print(f"  latest_md: {outputs['latest_md']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())