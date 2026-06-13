# Phase 33 Closeout

## 目标

用过去 7 天真实历史信息流做 time-sliced replay，验证自动选题、自动写稿、自动审稿和 final candidate 的连续产出质量。

## Historical Data Availability

新增历史数据可用性审计，按 D-7 到 D-1 生成 replay days。

## Time-sliced Replay Dataset

新增 `13_replay/replay_YYYYMMDD` dataset，按 cutoff 隔离每天可见数据。

## 7-day Topic Scoring Replay

新增 topic scoring replay，识别 main candidate、needs evidence、watch 和 metadata title 风险。

## 7-day Topic Selection Replay

新增 topic selection replay，统计 selected days、NO_QUALIFIED_TOPIC、重复选题和低证据选题。

## 7-day Brief / Outline / Draft Replay

新增 replay brief、outline、draft，draft 保持 `do_not_publish=true`。

## 7-day Review / Final Candidate Replay

新增 replay review 和 final candidate，final candidate 保持人工审阅。

## 7-day Quality Regression

新增 replay quality regression，检查 why now、核心读者问题、证据链、AI 味、伪造引用和 target price。

## Human Review Checklist

新增每天人工审核 checklist。

## Topic Quality Diagnosis

新增重复与低质量选题诊断。

## Calibration Proposals

新增 calibration proposals，全部 `auto_apply=false`。

## Workbench Replay Dashboard

Workbench 新增 7-Day Replay Trial Dashboard。

## Real Observation Checklist

新增真实 1-2 天 observation checklist。

## 本轮发现的最大问题

Replay 会暴露重复选题、metadata title 污染或证据门槛问题，并将其转成 sidecar calibration proposal。

## 是否建议进入真实 1-2 天观察

若 Go-Live Gate 仍至少为 `GO_LIVE_WITH_WARNINGS` 且 replay blocking failures 为 0，建议进入真实 1-2 天 observation。

## 是否建议进入 Phase 34

只有用户审阅并批准 calibration proposal 后，才进入 Phase 34：Apply Approved Calibration & Production Readiness Gate v1。
