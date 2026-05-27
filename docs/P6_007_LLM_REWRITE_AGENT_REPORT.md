# P6-007 LLM Rewrite Agent v1 Report

## 本轮目标

- 新增 LLM rewrite suggestion agent。
- 根据 revision instructions、critic/judge feedback 和 draft 生成改稿建议。
- 不自动覆盖原稿。

## 新增文件

- `src/content_system/llm_rewrite_agent.py`
- `scripts/run_llm_rewrite_suggestions.py`

## 输入

- `latest_revision_instructions.json`
- `latest_platform_packages.json`
- `latest_content_drafts.json`
- `latest_llm_critic_reviews.json`
- `latest_llm_judge_gate.json`

## 输出

- `05_draft_packs/*llm-rewrite-suggestions*.json`
- `05_draft_packs/*llm-rewrite-suggestions*.md`

## 新增命令

```bash
make llm-rewrite-suggestions
```

## 注意事项

所有建议都包含 `do_not_auto_apply=true`，后续改稿 loop 需另设 checkpoint。
