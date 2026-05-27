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
export THCAP_LLM_ENABLE_LIVE=0
export THCAP_LLM_MODE=dry_run
export THCAP_LLM_LIVE_AGENT_ALLOWLIST=
```

## 安全规则

- 不提交 API key。
- 不提交 `.env`。
- 不默认 live。
- 只允许 allowlist agent live。
- 当前只允许 `llm_proponent_agent` live pilot。
- live 失败必须 fallback。
- judge / critic / rewrite 不允许本阶段 live。
- rewrite suggestion 不自动覆盖原文。
- 不自动发布任何内容。

## 故障排查

- `missing MINIMAX_API_KEY`：设置本机环境变量后重试。
- `live not enabled`：确认 `THCAP_LLM_ENABLE_LIVE=1`。
- `mode not live`：确认 `THCAP_LLM_MODE=live`。
- `agent not allowlisted`：确认 `THCAP_LLM_LIVE_AGENT_ALLOWLIST=llm_proponent_agent`。
- `invalid JSON response`：系统会记录 validation issue 并 fallback。
- `HTTP timeout`：系统会记录 error 和 fallback reason。
- `provider returned non-200`：系统会记录 HTTP 状态和响应摘要。
