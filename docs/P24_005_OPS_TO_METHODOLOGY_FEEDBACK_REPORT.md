# P24-005 Ops-to-Methodology Feedback Report

## 目标

把 stable ops 中出现的内容质量、队列、日历和视觉问题反馈到方法论层。

## 实现

- 新增 `src/content_system/ops_to_methodology_feedback.py`。
- 新增 `scripts/build_ops_to_methodology_feedback.py`。
- 输出 topic/article/recipe/visual methodology feedback。

## 边界

所有建议 `auto_apply=false`；不自动改 config、prompt、rules 或 scoring rules。
