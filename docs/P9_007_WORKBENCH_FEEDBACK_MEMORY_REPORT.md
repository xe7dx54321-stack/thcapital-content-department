# P9-007 Workbench Feedback Memory v1 Report

## 本轮目标

将用户在工作台里的编辑反馈沉淀为偏好和规则建议输入。

## 新增文件

- `src/content_system/workbench_feedback_memory.py`
- `scripts/update_workbench_feedback_memory.py`

## 新增命令

```bash
make workbench-feedback-memory
```

## 记忆类型

- angle
- title
- evidence
- style
- topic
- risk
- platform

## 边界

只记录偏好，不自动修改规则或 prompt。
