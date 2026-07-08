#!/usr/bin/env python3
"""
P36-005: Run Production Readiness Gate
"""

import sys
sys.path.insert(0, '/workspace/src')

from pathlib import Path
from content_system.production_readiness_gate import (
    run_production_readiness_gate,
    save_readiness_gate
)


def main():
    output_dir = Path("/workspace/同行资本市场内容系统/10_logs")
    
    # Run gate with default parameters (cloud mode)
    result = run_production_readiness_gate(
        phase35_pass=True,
        phase34b_pass=True,
        phase34a_pass=True,
        phase33b_pass=True,
        usage_boundary_pass=True,
        no_secret_leak=True,
        no_openclaw_mod=True,
        auto_publish_disabled=True,
        workbench_ok=True,
        local_rss_smoke_done=False,
        runtime_observation_done=False,
        cloud_mode=True
    )
    
    outputs = save_readiness_gate(result, output_dir)
    
    print("Production Readiness Gate")
    print("=" * 40)
    print(f"overall_status: {result.overall_status}")
    print(f"pass_count: {result.pass_count}")
    print(f"warn_count: {result.warn_count}")
    print(f"fail_count: {result.fail_count}")
    print(f"blocking_failures: {result.blocking_failures}")
    print(f"ready_for_observation: {result.ready_for_observation}")
    print()
    print("Next Steps:")
    for step in result.next_steps:
        print(f"  - {step}")
    print()
    print("Output files:")
    print(f"  dated_json: {outputs['dated_json']}")
    print(f"  latest_json: {outputs['latest_json']}")
    print(f"  dated_md: {outputs['dated_md']}")
    print(f"  latest_md: {outputs['latest_md']}")
    
    # Return 0 for PASS, 0 for ACTIONABLE, 1 for FAIL
    if result.overall_status == "FAIL":
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())