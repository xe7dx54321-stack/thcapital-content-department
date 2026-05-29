# P16-006 Human Calibration Feedback Apply Report

## 本轮目标

记录用户对 live pilot 对比结果的校准反馈，供后续 prompt / methodology / recipe 调整参考。

## 已完成

- 新增 `record_live_calibration_feedback.py`。
- 支持 list / accept / reject / merge / defer。
- 新增 `live-calibration-board` 只读 Makefile 目标。

## 安全边界

- `auto_apply=false`。
- 不自动改 config、prompt 或 rules。
