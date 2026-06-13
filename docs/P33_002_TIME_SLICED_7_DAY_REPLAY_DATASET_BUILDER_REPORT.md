# P33-002 Time-sliced 7-day Replay Dataset Builder Report

## 目标

为过去 7 天生成独立 `replay_YYYYMMDD` dataset，每天只包含 cutoff 前可见数据。

## 输出

- `同行资本市场内容系统/13_replay/replay_YYYYMMDD/`
- `同行资本市场内容系统/10_logs/latest_time_sliced_replay_dataset.json`

## 边界

Replay dataset 不写入正式 topic、brief、draft 或 final candidate latest 文件。
