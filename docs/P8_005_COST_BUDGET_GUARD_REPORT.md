# P8-005 Cost Budget Guard v1 Report

## 本轮目标

统一读取 LLM provider config 与 agent run log，生成每日成本和调用次数保护报告。

## 新增文件

- `src/content_system/cost_budget_guard.py`
- `scripts/check_cost_budget_guard.py`

## 新增命令

```bash
make cost-budget-guard
```

## 环境变量

- `THCAP_LLM_DAILY_COST_LIMIT_USD`
- `THCAP_LLM_MAX_CALLS_PER_DAY`

## 输出结果

状态为 `ALLOW`、`WARN` 或 `BLOCK`。超限时建议 `recommended_mode = dry_run`。

## 边界

本轮只做保护报告与可复用函数，不自动修改 provider config，不自动启停 live mode。
