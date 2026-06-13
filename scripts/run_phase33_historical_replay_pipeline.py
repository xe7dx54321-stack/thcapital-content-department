#!/usr/bin/env python3
from pathlib import Path
import json
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from content_system.paths import get_project_paths
from content_system.phase33_historical_replay import run_phase33_historical_replay_pipeline

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    payload, _ = run_phase33_historical_replay_pipeline(get_project_paths(root), root)
    print(json.dumps(payload.get("summary", {}), ensure_ascii=False))
    print(f"status: {payload.get('status')}")
