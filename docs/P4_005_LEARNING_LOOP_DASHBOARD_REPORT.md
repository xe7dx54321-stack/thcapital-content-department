# P4-005 Learning Loop Dashboard v1 Report

## 目标

- 生成反馈学习看板。
- 展示发布候选、待反馈、历史结果、反馈标签和规则建议。

## 新增文件

- `src/content_system/learning_loop_dashboard.py`
- `scripts/build_learning_loop_dashboard.py`

## 新增命令

```bash
make learning-loop-dashboard
```

## 输出

- `同行资本市场内容系统/10_logs/*learning-loop-dashboard*.json`
- `同行资本市场内容系统/11_frontstage/*learning-loop-dashboard*.md`

## 验收

- `make learning-loop-dashboard` 可生成 JSON 和 frontstage Markdown。
