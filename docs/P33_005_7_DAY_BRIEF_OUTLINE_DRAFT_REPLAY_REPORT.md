# P33-005 7-day Brief / Outline / Draft Replay Report

## 目标

对有合格 main topic 的 replay day 生成 brief、outline 和 draft。

## 输出

- `同行资本市场内容系统/13_replay/replay_YYYYMMDD/briefs.json`
- `同行资本市场内容系统/13_replay/replay_YYYYMMDD/outlines.json`
- `同行资本市场内容系统/13_replay/replay_YYYYMMDD/drafts.json`
- `同行资本市场内容系统/10_logs/latest_7day_content_generation_replay.json`

## 边界

Draft 始终 `do_not_publish=true`，并保留 known weaknesses。
