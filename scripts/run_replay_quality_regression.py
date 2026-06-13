#!/usr/bin/env python3
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from content_system.replay_quality_regression import run

if __name__ == "__main__":
    payload, _ = run(Path(__file__).resolve().parents[1])
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
