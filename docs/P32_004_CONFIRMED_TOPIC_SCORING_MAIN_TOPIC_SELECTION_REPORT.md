# P32-004 Confirmed Topic Scoring & Main Topic Selection Report

## 目标

对 connector / OpenClaw / acquisition bridge 产出的候选选题进行自动评分，并选择当天主选题与备选题。

## 输出

- `同行资本市场内容系统/03_topic_candidates/latest_autonomous_topic_scores.json`
- `同行资本市场内容系统/03_topic_candidates/latest_daily_main_topic_selection.json`

## 边界

不强行每天选主选题；证据弱或 weak signal 未确认时只能进入 `NEEDS_EVIDENCE` / `WATCH`。
