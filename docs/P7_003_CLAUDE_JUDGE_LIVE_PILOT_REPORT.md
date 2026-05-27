# P7-003 Claude Judge Live Adapter Pilot Report

## 本轮目标

为 `llm_judge_agent` 增加 Claude live pilot，同时保持 rule judge 为权威结果。

## 修改文件

- `src/content_system/llm_judge_agent.py`
- `src/content_system/llm_agent_client.py`
- `scripts/run_llm_judge_gate.py`
- `scripts/run_claude_judge_live_pilot.py`

## Live Safety Design

- 默认 dry-run。
- live 必须显式设置 `THCAP_LLM_ENABLE_LIVE=1`、`THCAP_LLM_MODE=live` 和 allowlist。
- Judge live 只写 `latest_llm_judge_gate.json`。
- Judge live 不覆盖 rule judge，不改变 publishing queue。
- 冲突只进入 comparison 和 human spot-check 建议。

## New Command

```bash
make claude-judge-live-pilot
```

## Validation

- 无 key 或未 allowlist 时输出 `READY_CHECK_FAILED`，不崩溃。
- live 失败时 fallback 并写 agent run log。

## What Is Still Dry-run

- `phase6-daily` 和 `learning-daily` 仍默认 dry-run。
- Rewrite、publish、rule update 不会被 judge live 自动修改。

## Next Step

P7-004：Claude Rewrite Live Pilot v1。
