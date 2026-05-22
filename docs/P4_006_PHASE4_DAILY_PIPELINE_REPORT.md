# P4-006 Phase 4 Daily Pipeline v1 Report

## 目标

- 新增 Phase 4 日常入口。
- 串联 Phase 3 daily、publishing candidates、feedback template、feedback validation、outcome memory、rule suggestions 和 dashboard。

## 新增文件

- `scripts/run_phase4_daily_pipeline.py`

## 新增命令

```bash
make phase4-daily
```

## 验收

- `make phase4-daily` 成功或合理 DEGRADED，但不能崩溃。
- 没有人工反馈时保持 `UNREVIEWED` / `PENDING`。
