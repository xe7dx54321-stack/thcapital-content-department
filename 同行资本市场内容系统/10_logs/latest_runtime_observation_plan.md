# Runtime Observation Plan

## 概述

- **生成时间**: 2026-07-08T03:14:54.072405
- **需要 Mac Runtime**: False
- **观察天数**: 2
- **状态**: plan_generated

## Runtime 检查清单

| Check | 名称 | 命令 | 期望结果 | 云端说明 |
|-------|------|------|----------|----------|
| runtime_status | 检查 Runtime status | `python3 scripts/runtime_control.py status` | running_or_idle | 云端不要求真实 Runtime |
| launchagent_status | 检查 LaunchAgent status | `launchctl list | grep thcapital` | loaded_or_not_required | 云端不要求 launchd |
| heartbeat_age | 检查 heartbeat age | `检查 heartbeat 文件时间戳` | within_24h | 云端不要求真实 heartbeat |
| next_scheduled | 检查下次定时运行 | `检查 cron 或 launchd 配置` | configured | 云端不要求定时配置 |
| today_capture | 检查今日采集任务 | `make phase34a-daily` | success | 云端可执行 |
| today_topic_to_article | 检查今日 topic-to-article | `make phase32-daily` | success_or_empty | 云端可执行 |
| today_workbench | 检查今日 Workbench | `make wechat-workbench` | visible | 云端可执行 |
| retry_queue | 检查 retry queue | `检查 retry 状态` | empty_or_managed | 云端不要求真实 queue |
| missed_run | 检查 missed-run catch-up | `检查遗漏任务` | none_or_recovered | 云端不要求真实 catch-up |
| observation_period | 观察 1-2 天 | `每日运行 phase36-daily` | stable | 建议本地执行 |

## 命令参考

- `make runtime-go-live-validate`
- `make runtime-go-live-observation`
- `make runtime-go-live-acceptance`
- `make phase36-daily`
- `make wechat-workbench`
- `python3 scripts/runtime_control.py status`
- `python3 scripts/runtime_control.py pause`
- `python3 scripts/runtime_control.py resume`

## 观察流程

### 1. 启动观察

```bash
make runtime-go-live-observation
make phase36-daily
```

### 2. 每日检查

每日运行以下命令检查系统状态：

```bash
make phase34a-daily
make phase32-daily
make wechat-workbench
python3 scripts/runtime_control.py status
```

### 3. 观察期结束验收

```bash
make runtime-go-live-acceptance
```

## 统计

- **检查项总数**: 10

---

**Phase36** | Runtime Observation Plan
