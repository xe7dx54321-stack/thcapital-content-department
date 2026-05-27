# P6-010 Phase 6 Daily Agent Pipeline v1 Report

## 本轮目标

- 新增 Phase 6 日常总入口。
- 默认 mock/dry-run 跑通 LLM Agent 链路。
- 不需要 API key，不做真实 live 调用。

## 新增文件

- `scripts/run_phase6_daily_agent_pipeline.py`

## 执行链路

1. `run_learning_daily_pipeline.py`
2. `validate_llm_provider_config.py`
3. `validate_agent_prompts.py`
4. `run_llm_proponent_reviews.py`
5. `run_llm_critic_reviews.py`
6. `run_llm_judge_gate.py`
7. `run_llm_rewrite_suggestions.py`
8. `build_agent_run_summary.py`
9. `build_agent_evaluation_template.py`

## 输出

- `10_logs/*phase6-daily-agent-pipeline*.json`
- `10_logs/*phase6-daily-agent-pipeline*.md`
- `11_frontstage/*phase6-daily-agent-pipeline-board.md`

## 新增命令

```bash
make phase6-daily
```

## 验收方式

- `python3 -m py_compile scripts/run_phase6_daily_agent_pipeline.py`
- `make phase6-daily`
