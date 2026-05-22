# P3-008 Phase 3 Daily Review Pipeline v1 Report

## 本轮目标

- 新增 Phase 3 日常总入口。
- 串联 Phase 2 daily pipeline、review queue、proponent、critic、judge、revision、human exception queue 和 dashboard。

## 新增文件

- `scripts/run_phase3_daily_pipeline.py`

## 新增命令

```bash
make phase3-daily
```

## 执行链路

1. `scripts/run_phase2_daily_pipeline.py`
2. `scripts/build_agent_review_queue.py`
3. `scripts/build_proponent_reviews.py`
4. `scripts/build_critic_reviews.py`
5. `scripts/build_judge_gate.py`
6. `scripts/build_revision_instructions.py`
7. `scripts/build_human_exception_queue.py`
8. `scripts/build_agent_review_dashboard.py`

## 输出产物

- `同行资本市场内容系统/10_logs/*phase3-daily-pipeline*.json`
- `同行资本市场内容系统/10_logs/*phase3-daily-pipeline*.md`
- `同行资本市场内容系统/11_frontstage/*phase3-daily-pipeline*.md`

## 验收方式

- `python3 -m py_compile scripts/run_phase3_daily_pipeline.py`
- `make phase3-daily`

## 注意事项

如果上游没有 platform packages，但脚本正常生成空结果，应为合理 DEGRADED，不应崩溃。
