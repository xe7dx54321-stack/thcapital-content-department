#!/usr/bin/env python3
"""
P36-006: Build Rollback Safety Runbook
"""

import sys
sys.path.insert(0, '/workspace/src')

from pathlib import Path
from content_system.rollback_safety_runbook import (
    build_rollback_safety_runbook,
    save_rollback_runbook
)


def main():
    output_dir = Path("/workspace/同行资本市场内容系统/10_logs")
    
    result = build_rollback_safety_runbook()
    outputs = save_rollback_runbook(result, output_dir)
    
    print("Rollback Safety Runbook")
    print("=" * 40)
    print(f"section_count: {result.section_count}")
    print(f"contains_pause_resume: {result.contains_pause_resume}")
    print(f"contains_disable_rss: {result.contains_disable_rss}")
    print(f"status: {result.status}")
    print()
    print("Output files:")
    print(f"  dated_json: {outputs['dated_json']}")
    print(f"  latest_json: {outputs['latest_json']}")
    print(f"  dated_md: {outputs['dated_md']}")
    print(f"  latest_md: {outputs['latest_md']}")
    print(f"  docs_md: {outputs['docs_md']}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())