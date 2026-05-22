# P4/P5 Learning Daily Pipeline Report

## 目标

- 新增总入口 `make learning-daily`。
- 串联 Phase 3 Agent Review、Phase 4 发布准备与反馈学习、Phase 5 头部内容学习反哺。

## 新增文件

- `scripts/run_learning_daily_pipeline.py`

## 新增命令

```bash
make learning-daily
```

## 输出

- `同行资本市场内容系统/10_logs/*learning-daily-pipeline*.json`
- `同行资本市场内容系统/10_logs/*learning-daily-pipeline*.md`
- `同行资本市场内容系统/11_frontstage/*learning-daily-pipeline*.md`

## 验收

- `make learning-daily` 成功或合理 DEGRADED，但不能崩溃。
- generated artifacts 不进入 Git。
