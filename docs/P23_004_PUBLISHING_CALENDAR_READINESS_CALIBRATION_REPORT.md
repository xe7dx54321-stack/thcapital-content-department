# P23-004 Publishing Calendar Readiness Calibration Report

## 目标

校准 weekly publishing calendar 的 ready/open/hold 状态，明确每一天为什么不 ready，以及哪些日期可以通过人工动作变成 actionable。

## 实现

- 新增 `src/content_system/publishing_calendar_readiness_calibration.py`。
- 新增 `scripts/calibrate_publishing_calendar_readiness.py`。
- 输出 `READY|ACTIONABLE|HOLD|OPEN|NEEDS_REVIEW|NO_READY_CONTENT` 状态。

## 边界

不强行制造 ready day；当没有真正 ready 内容时，输出 `ACTIONABLE` 和 required operator action。
