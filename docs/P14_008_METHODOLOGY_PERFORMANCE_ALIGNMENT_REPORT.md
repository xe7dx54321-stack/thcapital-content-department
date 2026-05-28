# P14-008 Methodology Performance Alignment Report

## 本轮目标

把内容方法论与发布表现反馈对齐，判断哪些方法论维度可能与真实表现相关。

## 修改文件

- `src/content_system/methodology_performance_alignment.py`
- `scripts/build_methodology_performance_alignment.py`

## 输出

- `同行资本市场内容系统/10_logs/latest_methodology_performance_alignment.json`
- `同行资本市场内容系统/11_frontstage/latest_methodology_performance_alignment_board.md`

## 核心能力

- 汇总 topic/article/performance 记录数量。
- 生成 dimension insights、recipe insights 和 recommendations。
- 所有建议默认 `auto_apply=false`。

## 边界

只生成建议，不自动修改 methodology config、scoring rules、prompt 或 recipe。
