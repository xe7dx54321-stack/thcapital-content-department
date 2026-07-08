#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from content_system.narrative_frameworks import validate_narrative_frameworks
import json
from datetime import datetime


def main():
    result = validate_narrative_frameworks()

    print("Narrative Frameworks Validation")
    print("===============================")
    print(f"valid: {result['valid']}")
    print(f"framework_count: {result['framework_count']}")
    print(f"validated_count: {result['validated_count']}")
    print(f"errors: {result['errors']}")
    print(f"warnings: {result['warnings']}")

    run_date = datetime.now().strftime("%Y%m%d")
    logs_root = "同行资本市场内容系统/10_logs"
    os.makedirs(logs_root, exist_ok=True)

    dated_path = os.path.join(logs_root, f"{run_date}__narrative-frameworks-validation.json")
    latest_path = os.path.join(logs_root, "latest_narrative_frameworks_validation.json")

    with open(dated_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nOutput files:")
    print(f"  dated_json: {dated_path}")
    print(f"  latest_json: {latest_path}")

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
