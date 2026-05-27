# P7-004 Claude Rewrite Live Pilot Report

## 本轮目标

为 `llm_rewrite_agent` 增加 Claude live pilot，用于生成改稿建议。

## 修改文件

- `src/content_system/llm_rewrite_agent.py`
- `scripts/run_llm_rewrite_suggestions.py`
- `scripts/run_claude_rewrite_live_pilot.py`

## Live Safety Design

- 默认 dry-run。
- live 必须显式设置 env 和 allowlist。
- Rewrite live 只生成 suggestion。
- 不覆盖 brief、outline、draft、platform package。
- 输出中固定记录 `do_not_auto_apply=true`、`must_not_overwrite_original=true`。

## New Command

```bash
make claude-rewrite-live-pilot
```

## Validation

- 无 key 或未 allowlist 时输出 `READY_CHECK_FAILED`，不崩溃。
- live 失败时 fallback 并写 agent run log。

## What Is Still Dry-run

- 默认 pipeline 不触发 rewrite live。
- 改稿建议不会自动应用。

## Next Step

P7-005：LLM Agent A/B Comparison v1。
