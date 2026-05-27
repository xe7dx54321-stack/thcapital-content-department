# P6-008 Agent Run Log / Cost / Error Tracking v1 Report

## 本轮目标

- 统一记录 LLM Agent 调用。
- 记录 mock/dry-run 运行、provider、model、mode、耗时、token 估算、成本估算、错误和 fallback。
- 生成每日 agent run summary。

## 新增文件

- `src/content_system/agent_run_log.py`
- `scripts/build_agent_run_summary.py`

## 输出

- `10_logs/agent_run_log.json`
- `10_logs/agent_run_log.md`
- `11_frontstage/agent_run_log_board.md`
- `10_logs/*agent-run-summary*.json`
- `10_logs/*agent-run-summary*.md`

## 新增命令

```bash
make agent-run-summary
```

## 当前限制

Phase 6 v1 的成本为估算字段，mock/dry-run 成本为 0。
