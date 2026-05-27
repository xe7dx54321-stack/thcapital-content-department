# LLM Live Mode Runbook

## 当前默认状态

系统默认使用 `mock` / `dry_run`，不真实调用模型 API。

`make phase6-daily` 会显式使用 dry-run LLM agent。真实调用只通过独立灰度命令开启。

## 如何启用 MiniMax Proponent Live Pilot

仅 P7-001 允许 `llm_proponent_agent` 使用 MiniMax live pilot。API key 只放在本机环境变量中，不写入仓库。

```bash
export MINIMAX_API_KEY="..."
export THCAP_LLM_ENABLE_LIVE=1
export THCAP_LLM_MODE=live
export THCAP_LLM_LIVE_AGENT_ALLOWLIST=llm_proponent_agent
make minimax-proponent-live-pilot
```

可选覆盖：

```bash
export MINIMAX_BASE_URL="https://api.minimax.io/v1"
export MINIMAX_MODEL="manimax-2.7"
```

## 如何关闭 live mode

```bash
unset MINIMAX_API_KEY
unset ANTHROPIC_API_KEY
export THCAP_LLM_ENABLE_LIVE=0
export THCAP_LLM_MODE=dry_run
export THCAP_LLM_LIVE_AGENT_ALLOWLIST=
```

## Claude Critic Live Pilot

默认不启用。P7-002 只允许 `llm_critic_agent` 使用 Claude live pilot。

启用方式：

```bash
export ANTHROPIC_API_KEY="..."
export THCAP_LLM_ENABLE_LIVE=1
export THCAP_LLM_MODE=live
export THCAP_LLM_LIVE_AGENT_ALLOWLIST=llm_critic_agent
make claude-critic-live-pilot
```

可选覆盖：

```bash
export ANTHROPIC_BASE_URL="https://api.anthropic.com"
export ANTHROPIC_MODEL="claude-sonnet-4.6"
```

关闭方式：

```bash
unset ANTHROPIC_API_KEY
export THCAP_LLM_ENABLE_LIVE=0
export THCAP_LLM_MODE=dry_run
export THCAP_LLM_LIVE_AGENT_ALLOWLIST=
```

## Claude Judge Live Pilot

默认不启用。P7-003 只允许 `llm_judge_agent` 做旁路 live 判断。

Judge live 不覆盖 `latest_judge_gate.json`，不改变 rule judge 决策，不改变 publishing candidate queue。若 live judge 与 rule judge 冲突，只记录 comparison 和 human spot-check 建议。

启用方式：

```bash
export ANTHROPIC_API_KEY="..."
export THCAP_LLM_ENABLE_LIVE=1
export THCAP_LLM_MODE=live
export THCAP_LLM_LIVE_AGENT_ALLOWLIST=llm_judge_agent
make claude-judge-live-pilot
```

## Claude Rewrite Live Pilot

默认不启用。P7-004 只允许 `llm_rewrite_agent` 生成改稿建议。

Rewrite live 不覆盖 `latest_content_drafts.json`、`latest_platform_packages.json`、`latest_content_outlines.json` 或 `latest_content_briefs.json`，只输出 `latest_llm_rewrite_suggestions.json`。

启用方式：

```bash
export ANTHROPIC_API_KEY="..."
export THCAP_LLM_ENABLE_LIVE=1
export THCAP_LLM_MODE=live
export THCAP_LLM_LIVE_AGENT_ALLOWLIST=llm_rewrite_agent
make claude-rewrite-live-pilot
```

## 安全规则

- 不提交 API key。
- 不提交 `.env`。
- 不默认 live。
- 只允许 allowlist agent live。
- 当前只允许 `llm_proponent_agent`、`llm_critic_agent`、`llm_judge_agent`、`llm_rewrite_agent` 通过独立 pilot 命令灰度 live。
- live 失败必须 fallback。
- judge live 只能旁路判断，不能覆盖 rule judge。
- rewrite live 只能生成建议，不能覆盖原文。
- rewrite suggestion 不自动覆盖原文。
- 不自动发布任何内容。

## 故障排查

- `missing MINIMAX_API_KEY`：设置本机环境变量后重试。
- `live not enabled`：确认 `THCAP_LLM_ENABLE_LIVE=1`。
- `mode not live`：确认 `THCAP_LLM_MODE=live`。
- `agent not allowlisted`：确认 `THCAP_LLM_LIVE_AGENT_ALLOWLIST=llm_proponent_agent`。
- `critic agent not allowlisted`：确认 `THCAP_LLM_LIVE_AGENT_ALLOWLIST=llm_critic_agent`。
- `judge agent not allowlisted`：确认 `THCAP_LLM_LIVE_AGENT_ALLOWLIST=llm_judge_agent`。
- `rewrite agent not allowlisted`：确认 `THCAP_LLM_LIVE_AGENT_ALLOWLIST=llm_rewrite_agent`。
- `invalid JSON response`：系统会记录 validation issue 并 fallback。
- `HTTP timeout`：系统会记录 error 和 fallback reason。
- `provider returned non-200`：系统会记录 HTTP 状态和响应摘要。
