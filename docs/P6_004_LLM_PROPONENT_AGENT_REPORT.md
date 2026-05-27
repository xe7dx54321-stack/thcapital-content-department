# P6-004 LLM Proponent Agent v1 Report

## 本轮目标

- 新增 LLM proponent agent。
- 从“为什么值得发”的角度生成结构化 review。
- 默认 mock/dry-run，保留 fallback。

## 新增文件

- `src/content_system/llm_proponent_agent.py`
- `scripts/run_llm_proponent_reviews.py`

## 输入

- `latest_agent_review_queue.json`
- `latest_platform_packages.json`
- `latest_content_briefs.json`
- `config/agent_prompts.json`
- `config/llm_providers.json`

## 输出

- `06_review_queue/*llm-proponent-reviews*.json`
- `06_review_queue/*llm-proponent-reviews*.md`

## 新增命令

```bash
make llm-proponent-reviews
```

## 注意事项

该输出是 LLM 旁路 review，不替代规则型 proponent review。
