# P3-007 Agent Review Dashboard v1 Report

## 本轮目标

- 生成每天给用户看的 Agent Review Dashboard。
- 汇总 approved、needs revision、hold、human exception、agent disagreement 和 next actions。

## 新增文件

- `src/content_system/agent_review_dashboard.py`
- `scripts/build_agent_review_dashboard.py`

## 新增命令

```bash
make agent-review-dashboard
```

## 输出产物

- `同行资本市场内容系统/10_logs/*agent-review-dashboard*.json`
- `同行资本市场内容系统/11_frontstage/*agent-review-dashboard*.md`

## 验收方式

- `python3 -m py_compile src/content_system/agent_review_dashboard.py`
- `python3 -m py_compile scripts/build_agent_review_dashboard.py`
- `make agent-review-dashboard`

## 注意事项

Dashboard 用于减少人工管理带宽，优先展示 Human Attention Required。
