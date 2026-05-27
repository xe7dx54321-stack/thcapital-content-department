# P6-005 LLM Critic Agent v1 Report

## 本轮目标

- 新增 LLM critic agent。
- 从证据、逻辑、标题、风险和平台适配角度给出建设性批评。
- 默认 mock/dry-run，保留 fallback。

## 新增文件

- `src/content_system/llm_critic_agent.py`
- `scripts/run_llm_critic_reviews.py`

## 输入

- `latest_agent_review_queue.json`
- `latest_platform_packages.json`
- `latest_content_quality_review.json`

## 输出

- `06_review_queue/*llm-critic-reviews*.json`
- `06_review_queue/*llm-critic-reviews*.md`

## 新增命令

```bash
make llm-critic-reviews
```

## 注意事项

批评输出必须是建设性建议，不做真实 LLM live 调用。
