# P6-006 LLM Judge Agent v1 Report

## 本轮目标

- 新增 LLM judge sidecar。
- 对比 LLM proponent / critic 和规则型 judge gate。
- 记录与规则裁判的差异，但不直接覆盖规则裁判。

## 新增文件

- `src/content_system/llm_judge_agent.py`
- `scripts/run_llm_judge_gate.py`

## 输入

- `latest_agent_review_queue.json`
- `latest_llm_proponent_reviews.json`
- `latest_llm_critic_reviews.json`
- `latest_judge_gate.json`
- `latest_platform_packages.json`

## 输出

- `06_review_queue/*llm-judge-gate*.json`
- `06_review_queue/*llm-judge-gate*.md`

## 新增命令

```bash
make llm-judge-gate
```

## 关键原则

LLM judge 是旁路评估。若与 rule judge 冲突，应记录 conflict 并建议人工抽检。
