# P33-009 Calibration Proposal Sidecar Report

## 目标

基于 replay 诊断生成校准建议 sidecar。

## 输出

- `同行资本市场内容系统/10_logs/latest_content_quality_calibration_proposals.json`
- `同行资本市场内容系统/10_logs/latest_content_quality_calibration_proposals.md`

## 边界

所有 proposal `auto_apply=false` 且 `requires_human_approval=true`。
