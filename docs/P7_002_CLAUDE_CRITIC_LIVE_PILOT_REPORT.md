# P7-002 Claude Critic Live Adapter Pilot Report

## 本轮目标

- 为 `llm_critic_agent` 增加 Claude live adapter。
- 默认继续保持 dry-run。
- live 必须显式开启，并且只允许 allowlist 中的 critic agent。
- 没有 API key 或 live 条件不满足时不崩溃。
- live 失败时 fallback，并写入 agent run log。

## 修改文件

- `config/llm_providers.json`
- `env.example`
- `src/content_system/llm_provider_config.py`
- `src/content_system/llm_agent_client.py`
- `src/content_system/llm_critic_agent.py`
- `scripts/run_llm_critic_reviews.py`
- `scripts/run_claude_critic_live_pilot.py`
- `Makefile`
- `.gitignore`
- `docs/LLM_LIVE_MODE_RUNBOOK.md`
- `docs/PROJECT_STATE.md`
- `docs/DEVELOPMENT_TASKS.md`

## Live Safety Design

- 默认 provider 仍为 `mock`。
- 默认 mode 仍为 `dry_run`。
- `make phase6-daily` 继续显式传入 `--mode dry_run`。
- Claude critic live 必须同时满足：
  - `THCAP_LLM_ENABLE_LIVE=1`
  - `THCAP_LLM_MODE=live`
  - `THCAP_LLM_LIVE_AGENT_ALLOWLIST` 包含 `llm_critic_agent`
  - `ANTHROPIC_API_KEY` 存在
  - provider 支持 live
- 不满足条件时输出 `READY_CHECK_FAILED` 或 dry-run fallback。

## New Command

```bash
make claude-critic-live-pilot
```

专用脚本：

```bash
python3 scripts/run_claude_critic_live_pilot.py
python3 scripts/run_claude_critic_live_pilot.py --json
python3 scripts/run_claude_critic_live_pilot.py --dry-run-check
```

## Validation

本轮验收重点：

- `make llm-critic-reviews` 默认 dry-run 通过。
- `make claude-critic-live-pilot` 无 key 时不崩溃。
- `make phase6-daily` 仍保持 dry-run。
- agent run log 记录 live attempted / succeeded / fallback reason。
- 不提交 API key 或 `.env`。

## What Is Still Dry-run

- `llm_judge_agent`
- `llm_rewrite_agent`
- `make phase6-daily`
- 所有发布、改稿覆盖、规则更新动作

## Next Step

P7-003：Claude Judge Live Adapter Pilot v1。Judge live 只能做旁路判断，不能直接覆盖 rule judge。
