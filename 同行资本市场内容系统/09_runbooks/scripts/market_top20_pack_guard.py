#!/usr/bin/env python3
"""market_top20_pack_guard.py
确保给定日期存在有效的 canonical Top20 初筛包。
若包不存在或为空骨架，写入基础结构。
"""
import sys
import os
from datetime import datetime

def main():
    date_str = None
    write_mode = False

    args = sys.argv[1:]
    for i, arg in enumerate(args):
        if arg == "--date" and i+1 < len(args):
            date_str = args[i+1]
        if arg == "--write":
            write_mode = True

    if not date_str:
        print("ERROR: --date required")
        sys.exit(1)

    token = date_str.replace("-", "")
    base = "/Users/apple/Documents/同行资本市场内容系统"
    pack_path = f"{base}/03_topic_candidates/{token}__top20-screening-pack.md"

    existing = ""
    try:
        with open(pack_path, "r", encoding="utf-8") as f:
            existing = f.read()
    except FileNotFoundError:
        existing = ""

    # 判断是否需要重建：空骨架或少于 500 字符
    needs_rebuild = (
        len(existing.strip()) < 500 or
        "## Top20 列表" in existing and existing.count("\n") < 10
    )

    if needs_rebuild and write_mode:
        today = datetime.now().strftime("%Y-%m-%d")
        content = f"""# Top20 初筛包 — {today}

> 生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M")} | market-scout day-mainline heartbeat
> 状态：pre-final（待 content-writer / editor 评审后升为 final）

## 评分标准说明

| 字段 | 说明 |
|---|---|
| score | 综合信号强度评分（10-50 分） |
| signal_reasons | 进入 Top20 的核心信号依据 |
| source_quality | 原始来源可信度 |
| visual_material | 视觉素材丰富度评估 |

## Top20 列表

（等待 morning_flash / official_update_lane / market_topic_capture 等上游车道素材汇入）

---
*本包由 market_top20_pack_guard.py 自动初始化于 {datetime.now().isoformat()}*
"""
        os.makedirs(os.path.dirname(pack_path), exist_ok=True)
        with open(pack_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"WRITTEN: {pack_path} ({len(content)} bytes)")
        sys.exit(0)
    elif needs_rebuild:
        print(f"STALE: {pack_path} ({len(existing)} bytes) - needs --write to rebuild")
        sys.exit(1)
    else:
        print(f"OK: {pack_path} ({len(existing)} bytes)")
        sys.exit(0)

if __name__ == "__main__":
    main()