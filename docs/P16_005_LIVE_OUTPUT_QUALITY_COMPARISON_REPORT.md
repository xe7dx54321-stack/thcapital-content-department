# P16-005 Live Output Quality Comparison Report

## 本轮目标

对比 rule-based / methodology-generated / live-generated 输出质量。

## 已完成

- 新增 `live_output_quality_comparison.py`。
- 输出 `latest_live_output_quality_comparison.json/md`。
- 覆盖 brief、draft、rewrite、visual prompt。

## 安全边界

- 质量对比只作为参考。
- 不自动 use live。
- 不替换主线产物。
