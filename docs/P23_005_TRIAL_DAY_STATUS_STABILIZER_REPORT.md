# P23-005 Trial Day Status Stabilizer Report

## 目标

减少 trial-day-run 的 DEGRADED 噪声，把 blocker、可行动 warning 和普通运营提示区分开。

## 实现

- 新增 `src/content_system/trial_day_status_stabilizer.py`。
- 新增 `scripts/stabilize_trial_day_status.py`。
- 当 blocker 为 0、ready actions 存在且 blocked actions 为 0 时，将 DEGRADED 校准为 `ACTIONABLE`。

## 边界

真实 blocker 不会被隐藏或降级。
