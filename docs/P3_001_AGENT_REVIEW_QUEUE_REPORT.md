# P3-001 Agent Review Queue v1 Report

## 本轮目标

- 将 Phase 2 的 platform packages 转成 Agent 审核队列。
- 标记质量状态、风险等级、优先级、source/evidence 覆盖和进入审核原因。
- 不自动发布，不改变 Phase 2 输出格式。

## 新增文件

- `src/content_system/agent_review_queue.py`
- `scripts/build_agent_review_queue.py`

## 新增命令

```bash
make review-queue
```

## 输出产物

- `同行资本市场内容系统/06_review_queue/*agent-review-queue*.json`
- `同行资本市场内容系统/06_review_queue/*agent-review-queue*.md`

## 验收方式

- `python3 -m py_compile src/content_system/agent_review_queue.py`
- `python3 -m py_compile scripts/build_agent_review_queue.py`
- `make review-queue`

## 注意事项

该队列是规则型 Agent workflow 的输入，不代表真实 LLM Agent 审核结论。
