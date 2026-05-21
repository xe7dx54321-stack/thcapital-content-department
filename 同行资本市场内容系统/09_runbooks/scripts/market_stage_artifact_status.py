#!/usr/bin/env python3
"""market_stage_artifact_status.py
检查指定 artifact 是否达到目标状态。
支持 --kind pack（Top20 初筛包）且 accept-state=final。
若包为空骨架或 pre-final 状态，返回 1。
"""
import sys
import os

def main():
    path = None
    kind = None
    accept_state = None

    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--path" and i+1 < len(args):
            path = args[i+1]
        if arg == "--kind" and i+1 < len(args):
            kind = args[i+1]
        if arg == "--accept-state" and i+1 < len(args):
            accept_state = args[i+1]

    if not path:
        print("ERROR: --path required")
        sys.exit(1)

    if not os.path.exists(path):
        print(f"NOT_FOUND: {path}")
        sys.exit(1)

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"READ_ERROR: {e}")
        sys.exit(1)

    size = len(content.strip())

    if kind == "pack":
        # final 判定：内容 > 1KB 且包含实际 Top20 条目（非仅骨架）
        if size < 1200:
            print(f"NON_FINAL: {path} ({size} bytes) - too small to be final")
            print(f"STATE: pre-final or skeleton")
            sys.exit(1)

        # 检查是否有实际内容行（非表头、非说明）
        lines = [l for l in content.split("\n") if l.strip() and not l.strip().startswith("#") and not l.strip().startswith("|") and "---" not in l]
        content_lines = [l for l in lines if any(c.isdigit() for c in l) or "score" in l.lower() or "signal" in l.lower()]

        if len(content_lines) < 5:
            print(f"NON_FINAL: {path} ({size} bytes) - missing actual entries")
            print(f"STATE: pre-final")
            sys.exit(1)

        print(f"FINAL: {path} ({size} bytes)")
        sys.exit(0)
    else:
        print(f"UNKNOWN_KIND: {kind}")
        sys.exit(1)

if __name__ == "__main__":
    main()