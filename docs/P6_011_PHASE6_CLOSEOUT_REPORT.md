# P6-011 Phase 6 Closeout Report

## Phase 6 v1 目标

Phase 6 v1 的目标是把当前规则型 proponent / critic / judge / rewrite 链路升级为可选真实 LLM、默认 mock/dry-run、安全可回退、可记录成本和错误的 Agent 基础设施。

## 已完成能力

- LLM provider config。
- Prompt registry。
- Mock/dry-run LLM agent client。
- LLM proponent agent。
- LLM critic agent。
- LLM judge sidecar。
- LLM rewrite suggestion agent。
- Agent run log。
- Cost / error tracking。
- Human-in-the-loop agent evaluation template。
- Phase 6 daily agent pipeline。

## 新增命令

```bash
make llm-config-validate
make agent-prompts-validate
make llm-agent-smoke
make llm-proponent-reviews
make llm-critic-reviews
make llm-judge-gate
make llm-rewrite-suggestions
make agent-run-summary
make agent-evaluation-template
make agent-evaluation-validate
make phase6-daily
```

## Provider / Prompt / Agent Architecture

- Provider 配置位于 `config/llm_providers.json`。
- Prompt 配置位于 `config/agent_prompts.json`。
- `llm_agent_client.py` 统一生成结构化 request / response。
- 四类 LLM Agent 输出独立 artifact，不覆盖 Phase 3 规则型结果。

## Mock / Dry-run Safety Policy

- 默认 provider 是 `mock`。
- 默认 mode 是 `dry_run`。
- 不需要 API key。
- 非 mock live provider 在 v1 中只是安全占位。

## Fallback Policy

- LLM 输出缺失关键字段时使用规则型 fallback。
- LLM judge 不覆盖 rule judge。
- LLM rewrite 不覆盖原稿。

## Agent Run Log

- 所有 LLM agent 调用写入 `agent_run_log.json`。
- 每日 summary 记录失败数、dry-run 数、fallback 数和成本估算。

## Human Evaluation

- `make agent-evaluation-template` 生成文件型人工评估模板。
- `make agent-evaluation-validate` 校验评分和 action。

## 当前限制

- 真实 live adapter 尚未启用。
- 没有真实付费模型调用。
- 没有自动发布。
- 没有数据库型长期记忆。
- 没有自动调度系统。

## 下一阶段建议

Phase 7：真实 LLM Live Mode 灰度与自动调度。

- P7-001：OpenAI Live Adapter Pilot。
- P7-002：LLM Agent A/B Comparison。
- P7-003：Agent Rewrite Loop v1。
- P7-004：Daily Scheduler v1。
- P7-005：Failure Notification v1。
- P7-006：Retry / Fallback Runner v1。
- P7-007：Weekly Content Retro v1。
