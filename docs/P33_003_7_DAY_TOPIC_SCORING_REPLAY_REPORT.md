# P33-003 7-day Topic Scoring Replay Report

## 目标

对每个 replay day 独立运行 topic scoring，统计 main candidate、needs evidence、watch 和 metadata title 风险。

## 输出

- `同行资本市场内容系统/13_replay/replay_YYYYMMDD/topic_scores.json`
- `同行资本市场内容系统/10_logs/latest_7day_topic_scoring_replay.json`

## 边界

弱证据和 source metadata title 会被惩罚，不会被伪装成成熟选题。
